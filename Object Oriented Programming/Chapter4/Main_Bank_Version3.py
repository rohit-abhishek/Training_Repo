from Accounts import * 

account_dict = {}
next_account_number = 0 

# create two accounts 
o_joes_account = Accounts('Joe', 100, 'apple')
o_joes_account_nbr = next_account_number
next_account_number += 1
account_dict[o_joes_account_nbr] = o_joes_account


o_mary_account = Accounts('Mary', 500, 'orange')
o_mary_account_nbr = next_account_number
next_account_number += 1
account_dict[o_mary_account_nbr] = o_mary_account

# run some deposit and withdrawl transactions 
account_dict[o_joes_account_nbr].deposit(50, 'apple')
account_dict[o_mary_account_nbr].withdraw(20, 'orange')
account_dict[o_mary_account_nbr].deposit(500, 'orange')

# lets create accounts on fly 
print () 
user_name = input("Enter name of the new user account: ")
user_balance = input("Enter opening balance: ")
user_balance = int(user_balance)
user_password = input("Enter user password: ")

o_new_account = Accounts(user_name, user_balance, user_password)
o_new_account_nbr = next_account_number
next_account_number += 1
account_dict[o_new_account_nbr] = o_new_account

account_dict[o_new_account_nbr].getBalance(user_password)