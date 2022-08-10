import getpass

d = None


def loadtext(file, mode):
    try:
        with open(file, 'r') as f:
            x = f.readlines()
            if mode.lower() == 'return' or mode.lower() == 'r':
                return x
            else:
                for i in x:
                    print(i, end='')
    except:
        if mode.lower() == 'return' or mode.lower() == 'r':
            return "Error Loading Text"
        else:
            print("Error Loading Text")


def savedpass(mode, data=None):
    try:
        if mode.lower() == 'g':
            with open('details.txt', 'r') as f:
                x = f.readlines()
                if len(x) == 3:
                    return tuple(x)
                else:
                    return 'error', "error", 'error'
        elif mode.lower() == 's':
            with open('details.txt', 'w') as f:
                f.writelines(data)
                f.flush()

    except:
        return 'error', "error", 'error'


def connect(connector):
    global d
    x = input("Do you want to load saved login credentials? Y/N: ")
    if x.lower() == 'y':
        hostname, username, passwd = savedpass('g')
    else:
        hostname = input("Enter Database Hostname: ")
        username = input("Enter Username: ")
        passwd = getpass.getpass('Enter password:')
    try:
        db = connector.connect(
            host=hostname.replace('\n', ''),
            user=username.replace('\n', ''),
            password=passwd.replace('\n', '')
        )

        print()
        print("Succesfully Connected To Database!")
        print()

        if x.lower() != 'y':
            c = input("Do you want to save your login credentials? Y/N: ")
            if c.lower() == 'y':
                savedpass('s', [hostname + '\n', username + '\n', passwd + '\n'])
        d = db
        return db
    except:
        print()
        print("Error Connecting to Database!")
        print()


def execute(cursor, command):
    cursor.execute(command)
    return cursor.fetchall()


def checkdb(db, database_name="store" , table_name="Inventory"):
    cur = db.cursor()
    data = execute(cur, 'show databases')
    dbs = tuple()
    exist = False
    for i in data:
        for j in i:
            if j not in dbs:
                dbs += (j,)

    for i in dbs:
        if i == database_name:
            exist = True

    if not exist:
        execute(cur, "create database store")
        execute(cur,"create table "+table_name+" (SNO integer(255) NOT NULL PRIMARY KEY,PRODUCTNAME varchar(30),MRP integer(255),PRICE integer(255),STOCK integer(255),AVAILABE varchar(4),EXPIARYDATE date,DISCOUNT integer(255),PROFITMARGIN integer(255))")
    else:
        execute(cur , 'use store')
        data = execute(cur ,"show tables")
        tbls = tuple()
        there = False

        for i in data:
            for j in i:
                if j not in tbls:
                    tbls += (j,)

        for i in tbls:
            if i == table_name:
                there = True

        if there:
            return
        else:
            execute(cur , 'use store')
            execute(cur,"create table " + table_name + " (SNO integer(255) NOT NULL PRIMARY KEY,PRODUCTNAME varchar(30),MRP integer(255),PRICE integer(255),STOCK integer(255),AVAILABE varchar(4),EXPIARYDATE date,DISCOUNT integer(255),PROFITMARGIN integer(255))")




def display():
    pass


def modify():
    pass


def search():
    pass


def process(option):
    if option == 1:
        display()
    elif option == 2:
        modify()
    elif option == 3:
        search()
