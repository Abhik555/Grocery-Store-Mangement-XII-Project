import mysql.connector as c
from Utils import *

isrunning = False
option = None


def app():
    global isrunning
    global option

    loadtext('WelcomeText.txt', 'p')
    db = connect(c)
    if db is not None:
        cur = db.cursor()
    else:
        print("Error Connecting to database Please Restart")
        return
    isrunning = True
    while isrunning:
        if option is None:
            loadtext('choice.txt', 'p')
            option = 0
        print()
        cm = input("Please Enter your Choice or Type Help for more information: ")
        if cm.lower() == "quit" or cm.lower() == 'q' or cm.lower() == "4":
            isrunning = False
        elif cm.lower() == "1":
            option = 1
        elif cm.lower() == "2":
            option = 2
        elif cm.lower() == "3":
            option = 3
        elif cm.lower() == "5" or cm.lower() == "help" or cm.lower() == "h":
            loadtext("help.txt", 'p')

        process(option)


if __name__ == "__main__":
    app()
    input("Press Enter to exit")
