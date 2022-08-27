import mysql.connector as c
from Utils import *
try:
    import tabulate as t
except:
    print('Missing Required Library: Tabulate (pip install tabulate)')
    input()

isrunning = False
option = None


def app():
    try:
        global isrunning
        global option

        loadtext('WelcomeText.txt', 'p')
        db = connect(c)
        if db is not None:
            cur = db.cursor()
        else:
            print("Error Connecting to database Please Restart")
            return
        checkdb(db)
        isrunning = True
        while isrunning:
            if option is None:
                loadtext('choice.txt', 'p')
                option = 0
            print()
            cm = input("Please Enter your Choice or Type Help for more information: ")
            if cm.lower() == "quit" or cm.lower() == 'q' or cm.lower() == "4":
                isrunning = False
                break
            elif cm.lower() == "1":
                option = 1
            elif cm.lower() == "2":
                option = 2
            elif cm.lower() == "3":
                option = 3
            elif cm.lower() == "5" or cm.lower() == "help" or cm.lower() == "h":
                loadtext("help.txt", 'p')

            process(option, db)
            input('Press enter to continue...')
            option = None
    except:
        print('Fatal Error Application has crashed!')
        input()


if __name__ == "__main__":
    app()
    print()
    input("Press Enter to exit")
