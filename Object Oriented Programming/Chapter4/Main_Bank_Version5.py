from Bank import * 

bank_object = Bank()

# create test accounts 
account_1 = bank_object.create_accounts("rohit", 10000000, "rohit")
account_2 = bank_object.create_accounts("abhishek", 999999999, "abhishek")

# iterate 
while True:
    print()

    print ('Enter b for balance')
    print ('Enter d for deposit')
    print ('Enter w for withdrawal')
    print ('Enter c for closing account')
    print ('Enter o for opening new account')
    print ('Enter s to list all accounts')
    print ('Enter q for quitting')

    action = input("Please enter your selection: ")
    action = action.lower()[0]

    if action == "b":
        bank_object.balance()
    elif action == "c":
        bank_object.close_account()
    elif action == "d":
        bank_object.deposit()
    elif action == "o":
        bank_object.open_account()
    elif action == "s":
        bank_object.show()
    elif action == "q":
        break 
    elif action == "w":
        bank_object.withdraw()
    else:
        print ("Invalid option.. Try again")
print ("Done")