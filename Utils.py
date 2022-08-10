import getpass


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
        return db
    except:
        print()
        print("Error Connecting to Database!")
        print()


def execute(cursor, command):
    cursor.execute(command)
    return cursor.fetchall()


def process(option):
    pass
