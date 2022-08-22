import getpass
from tabulate import tabulate

d = None


def load_data():
    try:
        with open('parameter.txt', 'r') as f:
            x = f.readlines()
            out = []
            for i in x:
                out.append(i.replace('\n', ''))
            return out
    except:
        print("Value not found error")


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


def checkdb(db, database_name=load_data()[0], table_name=load_data()[1]):
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

    if exist:
        return

    if not exist:
        execute(cur, "create database store")
        execute(cur,
                "create table " + table_name.lower() + " (SNO integer(255) NOT NULL PRIMARY KEY,PRODUCTNAME varchar(30),MRP integer(255),PRICE integer(255),STOCK integer(255),AVAILABE varchar(4),EXPIARYDATE date,DISCOUNT integer(255),PROFITMARGIN integer(255))")
    else:
        execute(cur, 'use store')
        data = execute(cur, "show tables")
        tbls = tuple()
        there = False

        for i in data:
            for j in i:
                if j not in tbls:
                    tbls += (j,)

        for i in tbls:
            if i == table_name.lower():
                there = True

        if there:
            return
        else:
            execute(cur, 'use store')
            execute(cur,
                    "create table " + table_name + " (SNO integer(255) NOT NULL PRIMARY KEY,PRODUCTNAME varchar(30),MRP integer(255),PRICE integer(255),STOCK integer(255),AVAILABE varchar(4),EXPIARYDATE date,DISCOUNT integer(255),PROFITMARGIN integer(255))")


def display(cur):
    execute(cur,'use '+load_data()[0])
    x = execute( cur,'select * from '+load_data()[1])
    print()
    print(tabulate(x , ['SNO' ,'PRODUCTNAME' ,'MRP' ,'PRICE' ,'STOCK' , 'AVAILABLE' , 'EXPIERYDATE','DISCOUNT', 'PROFIT MARGIN']))


def modify(cur):
    x = load_data()
    change_values('add', cur, x[0], x[1], (1, 'PRD 1', 200, 250, 1000, 'YES', '15-4-22', 5, 45))


def search(cur):
    pass


def change_values(action, cursor, db_name, table_name, values=None):
    if action.lower() == "add" or action.lower() == 'a':
        if values is None:
            return
        else:
            execute(cursor, 'use ' + db_name)
            execute(cursor, 'insert into ' + table_name + ' values' + str(values))


def process(option, db):
    if option == 1:
        display(db.cursor())
        db.commit()
    elif option == 2:
        modify(db.cursor())
        db.commit()
    elif option == 3:
        search(db.cursor())
        db.commit()


if __name__ == "__main__":
    load_data()
    input()
