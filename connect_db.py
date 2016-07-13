# sample-image-generator will use this scipt's return values to generate the images
# the script reads the query file, executes it line by line and returns the return values
import psycopg2


def generate_connect_str():
    with open('connect_str.txt', 'w') as connect_str:
        connect_values = []
        connect_inputs = ['dbname', 'user', 'password']
        for i in connect_inputs:
            connect_values.append("""{0}='{1}'""".format(i, input('Please enter your {0}: '.format(i))))
        connect_str.write("""{0} {1} host='localhost' {2}""".format(connect_values[0], connect_values[1], connect_values[2]))


def connect_params():
    with open('connect_str.txt', 'r') as connect_str:
        connect_str = connect_str.read()
        return connect_str


def sql_querys():
    query_values = []
    # opening the sql file that stores the querys as a list of strings
    # with open('querys.sql', 'r') as querys:
    #     query_strings = querys.readlines()
    # for i in query_strings:
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
        # sql querys as a string from an external sql file
        execute_string = """SELECT name FROM project;"""
        # running the querys
        cursor.execute(str(execute_string))
        # Fetch and print the result of the last execution
        rows = cursor.fetchall()
        # query_values.append(rows)
        print(rows)
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)
    # return query_values
sql_querys()
