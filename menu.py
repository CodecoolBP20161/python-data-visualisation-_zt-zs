import time
menu = True
while menu:
    print('''
    1. first menu item
    2. second menu item
    3. third menu item
    4. fourth menu item
    ''')
    menu = int(input('Select a menu option, please: '))
    if menu == 1:
        print('first')  # tag_cloud_1
    elif menu == 2:
        print('second')  # tag_cloud_2
    elif menu == 3:
        print('third')  # tag_cloud_3
    elif menu == 4:
        print('fourth')     # tag_cloud_4
    time.sleep(1)
