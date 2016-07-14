from connect_db import sql_queries
import time
queries = sql_queries()
menu = True
while menu:
    print('''
    1. client names tag-cloud based on the number of projects by a company
    2. project names tag-cloud based on the size of the budgets
    3. third menu item
    4. fourth menu item
    ''')
    menu = int(input('Select a menu option, please: '))
    if menu == 1:
        print(queries[0])  # tag_cloud_1
    elif menu == 2:
        print(queries[1])  # tag_cloud_2
    elif menu == 3:
        print(queries[2])  # tag_cloud_3
    elif menu == 4:
        print(queries[3])     # tag_cloud_4
    time.sleep(1)
