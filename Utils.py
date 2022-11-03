import getpass
from tabulate import tabulate


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

    if not exist:
        execute(cur, "create database store")
        execute(cur , 'use store')
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
    execute(cur, 'use ' + load_data()[0])
    x = execute(cur, 'select * from ' + load_data()[1])
    print()
    print(tabulate(x, ['SNO', 'PRODUCTNAME', 'MRP', 'PRICE', 'STOCK', 'AVAILABLE', 'EXPIERYDATE', 'DISCOUNT',
                       'PROFIT MARGIN']))
    print()


def modify(cur):
    print()
    v = input("Do you want to add a record or delete a record(Type Add or Delete or Edit): ")
    if v.lower() == 'add' or v.lower() == 'a':
        display(cur)
        print()
        SNO = input("Enter Product No(integer): ")
        PRODUCTNAME = input("Enter product name(text): ")
        MRP = input("Enter MRP(integer): ")
        PRICE = input("Enter Price(integer): ")
        STOCK = input("Enter Stock(integer): ")
        AV = input("Available(YES or NO): ")
        EXPIERYDATE = input("Enter ExpieryDate(Date: YYYY-MM-DD): ")
        DISCOUNT = input("Enter Discount(integer): ")
        PROFIT = input("Enter Profit Margin(integer): ")
        try:
            change_values(v, cur, (
                int(SNO), PRODUCTNAME, int(MRP), int(PRICE), int(STOCK), AV, EXPIERYDATE, int(DISCOUNT), int(PROFIT)))
        except:
            print()
            print('Operation Failed Input Data Error Pls check datatype of inputted values!')
            print()
            return
        print()
        print("Values Added!")
        print()
        display(cur)
    elif v.lower() == 'delete' or v.lower() == 'd':
        print()
        display(cur)
        n = int(input("Enter SNO of item you wish to delete: "))
        try:
            change_values(v, cur, n)
        except:
            print("Operation Failed!")
        print('Item Purged')
        display(cur)
    elif v.lower() == 'edit' or v.lower() == 'e':
        print()
        display(cur)
        print()
        x = load_data()
        no = input('Enter SNO of entry you want to edit: ')
        c = input("Enter column name(BE SPECIFIC): ")
        v = input("Enter new value: ")
        try:
            execute(cur, 'update ' + x[1] + ' set ' + c.upper() + '= "' + v + '" where SNO=' + no)
            print()
            display(cur)
            print()
        except Exception:
            print()
            print('Input Error')
            print()
            return
    else:
        return


def search(cur):
    print()
    c = None
    arg = None
    ch = input('Do you want all columns to display ? Y/N: ')
    if ch.lower() == 'n':
        c = []
        display(cur)
        print()
        while True:
            _ = input('Enter Column you want to display Name: ')
            c.append(_)
            e = input('Do you want continue? Y/N:')
            if e.lower() == 'no' or e.lower() == 'n':
                break
    ch1 = input('Do you want to enter a search query? Y/N: ')
    if ch1.lower() == 'y':
        arg = ''
        display(cur)
        print()
        while True:
            _ = input("Enter MYSQL Argument(EG: price > 100): ")
            arg += _
            e = input('Do you want to continue? Y/N:')
            if e.lower() == 'no' or e.lower() == 'n':
                break
            else:
                v = input('Do you want a AND Logical Operator or OR Logical Operator-> AND/OR/A/R: ')
                if v.lower() == 'and' or v.lower() == 'a':
                    arg += ' and '
                elif v.lower() == 'or' or v.lower() == 'r':
                    arg += ' or '
                else:
                    break
    print()
    find(cur, c, arg)


def find(cur, columns=None, condiitons=None):
    try:
        d = load_data()
        x = None
        selection = ''

        execute(cur, 'use ' + d[0])

        if columns is not None:
            for i in columns:
                if len(selection) == 0:
                    selection += i
                else:
                    selection += ',' + i
        if columns is None:
            if condiitons is None:
                x = execute(cur, 'select *' + ' from ' + d[1])
            else:
                x = execute(cur, 'select *' + ' from ' + d[1] + ' where ' + condiitons + ';')
        else:
            if condiitons is None:
                x = execute(cur, 'select ' + selection + ' from ' + d[1])
            else:
                x = execute(cur, 'select ' + selection + ' from ' + d[1] + ' where ' + condiitons + ';')
        print()
        if columns is not None:
            print(
                tabulate(x,
                         columns)
            )
        else:
            print(tabulate(x, ['SNO', 'PRODUCTNAME', 'MRP', 'PRICE', 'STOCK', 'AVAILABLE', 'EXPIERYDATE', 'DISCOUNT',
                               'PROFIT MARGIN']))
    except:
        print("Search Error Please Check Your Arguments For SQL Syntax Errors")



def change_values(action, cursor, values, db_name=load_data()[0], table_name=load_data()[1]):
    if action.lower() == "add" or action.lower() == 'a':
        if values is None:
            return
        else:
            execute(cursor, 'use ' + db_name)
            execute(cursor, 'insert into ' + table_name + ' values' + str(values))
    elif action.lower() == 'delete' or action.lower() == 'd':
        if values is None:
            return
        else:
            execute(cursor, 'use ' + db_name)
            execute(cursor, 'delete from ' + table_name + ' where SNO=' + str(values))


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
    input("This file cannot be run on its own Execute main.py!")
