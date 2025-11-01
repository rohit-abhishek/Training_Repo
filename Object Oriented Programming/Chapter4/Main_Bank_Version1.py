from Accounts import * 

# create two accounts 
o_joes_account = Accounts('Joe', 100, 'apple')
o_mary_account = Accounts('Mary', 500, 'orange')

# run some deposit and withdrawl transactions 
o_joes_account.deposit(50, 'apple')
o_mary_account.withdraw(20, 'orange')
o_mary_account.deposit(500, 'orange')

# lets create accounts on fly 
print () 
user_name = input("Enter name of the new user account: ")
user_balance = input("Enter opening balance: ")
user_balance = int(user_balance)
user_password = input("Enter user password: ")

o_new_account = Accounts(user_name, user_balance, user_password)
o_new_account.getBalance(user_password)