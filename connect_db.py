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


def sql_querys():
    num_of_querys = 2
    try:
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
        all_querys = []
        for i in range(num_of_querys):
            with open('query{0}.sql'.format(i + 1), 'r') as query_string:
                query_string = query_string.read()
            cursor.execute(str(query_string))
            all_querys.append(cursor.fetchall())
        # return the result of each executions as list of list of tuples
        return all_querys
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
sql_querys()
