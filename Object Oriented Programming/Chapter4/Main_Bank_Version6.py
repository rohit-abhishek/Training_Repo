from Bank import * 

oBank = Bank ("9 to 5", "123 Main Street, Anytown, USA", "(650) 555-12121")

while True:
    print () 
    print ('Enter b for balance')
    print ('Enter d for deposit')
    print ('Enter w for withdrawal')
    print ('Enter c for closing account')
    print ('Enter o for opening new account')
    print ('Enter s to list all accounts')
    print ('Enter q for quitting')
    print ()

    action = input("What do you want to do? ")
    action = action.lower()
    action = action[0]
    print ()

    try: 
        if action == "b":
            oBank.balance()
        elif action == "c":
            oBank.close_account()
        elif action == "d":
            oBank.deposit()
        elif action == "o":
            oBank.open_account()
        elif action == "s":
            oBank.show()
        elif action == "q":
            break 
        elif action == "w":
            oBank.withdraw()
    except AbortTransaction as e:
        print (e)

print ("Done")