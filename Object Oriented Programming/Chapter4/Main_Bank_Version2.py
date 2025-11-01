from Accounts import * 

account_list = [] 

# create two accounts 
o_joes_account = Accounts('Joe', 100, 'apple')
account_list.append(o_joes_account)
o_mary_account = Accounts('Mary', 500, 'orange')
account_list.append(o_mary_account)

# run some deposit and withdrawl transactions 
account_list[0].deposit(50, 'apple')
account_list[1].withdraw(20, 'orange')
account_list[1].deposit(500, 'orange')

# lets create accounts on fly 
print () 
user_name = input("Enter name of the new user account: ")
user_balance = input("Enter opening balance: ")
user_balance = int(user_balance)
user_password = input("Enter user password: ")

o_new_account = Accounts(user_name, user_balance, user_password)
account_list.append(o_new_account)
account_list[2].getBalance(user_password)