from Accounts import * 

account_dict = {} 
next_account_nbr = 0 

while True:
    print()

    print ('Enter b for balance')
    print ('Enter d for deposit')
    print ('Enter w for withdrawal')
    print ('Enter o for opening new account')
    print ('Enter q for quitting')

    action = input("Please enter your selection: ")

    if action == "b":
        print ("**** Get Balance ****")
        user_account_nbr = input("Enter your Account number: ")
        user_account_nbr = int(user_account_nbr)
        user_password = input("Enter your password: ")
        
        account_details = account_dict.get(user_account_nbr, None)

        if account_details:
            balance = account_details.getBalance(user_password)
        else: 
            print ("Invalid Account Number entered")

    elif action == "d":
        print ("**** Deposit ****")
        user_account_nbr = input("Enter your Account number: ")
        user_account_nbr = int(user_account_nbr)
        user_password = input("Enter your password: ")
        user_deposit_amount = input("Enter amount to deposit: ")
        user_deposit_amount = int(user_deposit_amount)
        
        account_details = account_dict.get(user_account_nbr, None)

        if account_details:
            balance = account_details.deposit(user_deposit_amount, user_password)
        else: 
            print ("Invalid Account Number entered")        

    elif action == "w":
        print ("**** Withdrawl ****")
        user_account_nbr = input("Enter your Account number: ")
        user_account_nbr = int(user_account_nbr)
        user_password = input("Enter your password: ")
        user_deposit_amount = input("Enter amount to withdraw: ")
        user_deposit_amount = int(user_deposit_amount)
        
        account_details = account_dict.get(user_account_nbr, None)

        if account_details:
            balance = account_details.withdraw(user_deposit_amount, user_password)
        else: 
            print ("Invalid Account Number entered")    

    elif action == "o":
        print ("**** Open Account ****")
        user_account_nbr = next_account_nbr
        next_account_nbr += 1
        user_name = input("Enter your name: ")
        user_password = input("Enter your password: ")
        user_deposit_amount = input("Enter your initial balance: ")
        user_deposit_amount = int(user_deposit_amount)
        
        new_account = Accounts(user_name, user_deposit_amount, user_password)
        account_dict[user_account_nbr] = new_account

        print ("Your account number is ", user_account_nbr)

    elif action == "q"     :
        break

    else: 
        print ("Invalid selection please try again")