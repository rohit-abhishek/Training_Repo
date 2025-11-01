from Accounts import * 

class Bank:
    def __init__(self) -> None:
        self.account_dict = {} 
        self.next_account_number = 0 

    def create_accounts(self, name, starting_amount, password):
        account_object = Accounts(name, starting_amount, password)
        account_number = self.next_account_number
        self.account_dict[account_number] = account_object
        self.next_account_number += 1
        return account_number
    
    def open_account(self):
        print ("*** Open Account ***")
        user_name = input("What is the name of the account: ")
        user_starting_amount = input("What is the starting balance: ")
        user_starting_amount = int(user_starting_amount)
        user_password = input("Enter your password: ")

        user_account_number = self.create_accounts(user_name, user_starting_amount, user_password)
        print ("Account Opened. Your Account number is: ", user_account_number)

        print ()

    def close_account(self):
        print ("*** Close Account ***")
        user_account_number = input("Enter your account number: ")
        user_account_number = int(user_account_number)
        user_password = input("Enter your password: ")
        account_object = self.account_dict.get(user_account_number)
        account_balance = account_object.getBalance(user_password)

        if account_balance:
            # print ("Your balance is ", account_balance, " which will be returned on closure")
            del self.account_dict[user_account_number]
            print ("Account ", user_account_number, " is closed now ")

    def balance(self):
        print ("*** Get Balance ***")
        user_account_number = input("Enter your account number: ")
        user_account_number = int(user_account_number)
        user_password = input("Enter your password: ")
        account_object = self.account_dict.get(user_account_number)
        account_balance = account_object.getBalance(user_password)

        # if account_balance:
        #     print ("Your Balance is: ", account_balance)

    def deposit(self):
        print ("*** Amount Deposit ***")
        user_account_number = input("Enter your account number: ")
        user_account_number = int(user_account_number)
        user_password = input("Enter your password: ")
        user_deposit_amount = input("Enter Amount to be deposit: ")
        user_deposit_amount = int(user_deposit_amount)
        account_object = self.account_dict.get(user_account_number)

        account_balance = account_object.deposit(user_deposit_amount, user_password)
                
    def show(self): 

        for user_account_number in self.account_dict:
            account_object = self.account_dict.get(user_account_number)
            print ("User Account Number: ", user_account_number)
            account_object._show()

    def withdraw(self):
        print ("*** Withdraw Amount ***")

        user_account_number = input("Enter your account number: ")
        user_account_number = int(user_account_number)
        user_password = input("Enter your password: ")
        user_withdraw_amount = input("Enter Amount to be withdraw: ")
        user_withdraw_amount = int(user_withdraw_amount)

        account_object = self.account_dict.get(user_account_number)

        user_balance = account_object.withdraw(user_withdraw_amount, user_password)


if __name__ == "__main__":

    bank_object_1 = Bank()
    for i in range (2):
        bank_object_1.open_account()

    bank_object_1.show()

    bank_object_1.deposit()
    bank_object_1.balance()
    bank_object_1.withdraw()
    bank_object_1.balance()

    bank_object_1.show()