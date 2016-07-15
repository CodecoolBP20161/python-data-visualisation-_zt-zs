from connect_db import sql_queries
import image_generator
import time


queries = sql_queries()
menu = 0
while not menu:
    print('''
    1. client names tag-cloud based on the number of projects by a company
    2. project names tag-cloud based on the size of the budgets
    3. client names tag-cloud based on the IDs of the projects
    4. client HQ tag-cloud
    5. manager names tag-cloug
    ''')
    menu = int(input('Select a menu option, please: '))
    if menu == 1:
        image = image_generator.Text.output(sql_queries(), 0)
        image_generator.Text.sizing(image)
        image_generator.print_text(image, "companies")
    elif menu == 2:
        image = image_generator.Text.output(sql_queries(), 1)
        image_generator.Text.sizing(image)
        image_generator.print_text(image, "projects")
    elif menu == 3:
        image = image_generator.Text.output(sql_queries(), 2)
        image_generator.Text.sizing(image)
        image_generator.print_text(image, "clients")
    elif menu == 4:
        image = image_generator.Text.output(sql_queries(), 3)
        image_generator.Text.sizing(image)
        image_generator.print_text(image, "company_hq")
    elif menu == 5:
        image = image_generator.Text.output(sql_queries(), 4)
        image_generator.Text.sizing(image)
        image_generator.print_text(image, "managers")


