# sample-image-generator will use this scipt's return values to generate the images
# the script reads the query file, executes it line by line
# return value is a list of lists(sql querys) of tuples(sql query return values)
import psycopg2


# generating local connect string into a txt file
def generate_connect_str():
    connect_values = []
    connect_inputs = ['dbname', 'user', 'password']
    for i in connect_inputs:
        connect_values.append("""{0}='{1}'""".format(i, input('Please enter your {0}: '.format(i))))
    with open('connect_str.txt', 'w') as connect_str:
        connect_str.write("""{0} {1} host='localhost' \
{2}""".format(connect_values[0], connect_values[1], connect_values[2]))


# reading connect string from local txt file
def connect_params():
    with open('connect_str.txt', 'r') as connect_str:
        connect_str = connect_str.read()
        return connect_str


# converting hex values to rgb triplets
def hex_to_rgb(color_comps):
    if color_comps:
        if len(color_comps) > 4:
            color_comps = color_comps.split()
            rgb_colors = []
            for hex_value in color_comps:
                hex_value = hex_value.lstrip('#')
                lv = len(hex_value)
                rgb_colors.append(tuple(int(hex_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))
            if len(rgb_colors) > 1:
                color_counter = 0
                avg_color = [0, 0, 0]
                for triplet in rgb_colors:
                    color_counter += 1
                    for i in range(0, 3):
                        avg_color[i] += triplet[i]
                # for i in avg_color:
                #     # i /= color_counter
                #     i += 100
                return tuple(avg_color)
            else:
                return rgb_colors[0]
        else:
            return color_comps
    else:
        return(0, 0, 0)


def sql_queries():
    num_of_queries = 4
    # setup connection string
    try:
        connect_str = str(connect_params())
    except Exception:
        generate_connect_str()
        connect_str = str(connect_params())
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # set autocommit option, to do every query when we call it
    conn.autocommit = True
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # read sql query strings from external sql files and execute them
    all_queries = []
    for i in range(num_of_queries):
        with open('query{0}.sql'.format(i + 1), 'r') as query_string:
            query_string = query_string.read()
        cursor.execute(str(query_string))
        all_queries.append(cursor.fetchall())
    # convert hex color values to averaged rgb triplets
    new_queries = []
    for query in all_queries:
        new_cases = []
        for case in query:
            new_cases.append(tuple([case[0], case[1], hex_to_rgb(case[2])]))
        new_queries.append(new_cases)
    # return the result of each executions as list of list of tuples
    return new_queries
