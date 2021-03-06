# This file started as a simple database connect string generator,
# but ended up being much more than that.
# As of now, in addition of generating the local database connect string,
# it also executes the sql queries and transforms their hex colors to
# single, averaged rgb triplets.
# menu.py uses its return values (a list of lists of tuples from sql_queries())
# to call image-generator1.py with.
import psycopg2
import random


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
        color_comps = color_comps.split()
        rgb_colors = []
        for hex_value in color_comps:
            hex_value = hex_value.lstrip('#')
            lv = len(hex_value)
            rgb_colors.append(tuple(int(hex_value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)))
            color_counter = 0
            avg_color = [0, 0, 0]
            for triplet in rgb_colors:
                color_counter += 1
                for i in range(0, 3):
                    avg_color[i] += triplet[i]*17
            for i in avg_color:
                i /= color_counter
            return tuple(avg_color)
    else:
        # returns with black color, if no color given
        return(255, 255, 255)


# main function
def sql_queries():
    num_of_queries = 5
    # setup connection string
    try:
        connect_str = str(connect_params())
    except Exception:
        generate_connect_str()
        connect_str = str(connect_params())
    # use our connection values to establish a connection
    try:
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
        # convert hex color values to averaged rgb triplets and add dogenator
        dogenator = ['such', 'much', 'wow']
        new_queries = []
        for query in all_queries:
            new_cases = []
            for case in query:
                new_cases.append(tuple(['{0} \
    {1}'.format(dogenator[random.randint(0, 2)], case[0]), case[1], hex_to_rgb(case[2])]))
            new_queries.append(new_cases)
        # return the result of each executions as list of list of tuples
        return new_queries
    except Exception:
        print("Cannot connect database. Edit 'connect_str.txt' to fix possible typos, then run the program again.")
