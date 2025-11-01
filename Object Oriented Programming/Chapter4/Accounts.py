class AbortTransaction (Exception):
    pass


class Accounts:

    # initialize the properties - Keep them protected 
    def __init__(self, name, balance, password):
        self.__name = name
        self.__balance = int(balance)
        self.__prev_balance = int(balance)
        self.__password = password 
    
    # set getter and setter for name 
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        if name != None and name != "":
            self.__name = name
    
    # set getter and setter for balance 
    @property
    def prev_balance(self):
        return self.__prev_balance
    
    @prev_balance.setter
    def balance(self, amt_balance):
        try: 
            self.__prev_balance = int(amt_balance)
        except (TypeError, ValueError) as e:
            raise type(e) ('Balance: ' + str(amt_balance) + ', is invalid ')

        if amt_balance < 0: 
            raise AbortTransaction ('Balance: ' + str(amt_balance) + ', cannot be negative')

    # set getter and setter for balance 
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, amt_balance):
        try: 
            self.__balance = int(amt_balance)
        except (TypeError, ValueError) as e:
            raise type(e) ('Balance: ' + str(amt_balance) + ', is invalid ')

        if amt_balance < 0: 
            raise AbortTransaction ('Balance: ' + str(amt_balance) + ', cannot be negative')



    # set getter and setter for balance 
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, pass_str):
        if not pass_str:
            raise TypeError ('Please enter the password')
        self.__password = pass_str

    def validate_amount(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            raise AbortTransaction("Amount must be integer")
        
        if amount <= 0: 
            raise AbortTransaction("Amount must be positive")

        return amount
    
    def check_password_match(self, password):
        if password != self.password:
            raise AbortTransaction ("Invalid Password Entered")


    def deposit(self, amount_to_deposit, password):

        if password != self.password:
            print ("Invalid Password")
            return None 
        
        if amount_to_deposit < 0: 
            print("You cannot deposit negative amount")
            return None 
        
        self.__prev_balance = self.balance
        self.balance = self.balance + amount_to_deposit
        self.__show('deposit')
        return self.balance 
    
    def withdraw(self, amount_to_withdraw, password): 

        if amount_to_withdraw < 0: 
            print ("You cannot withdraw negative amount")
            raise AbortTransaction ("amount to withdraw cannot be negative")

        if amount_to_withdraw > self.balance: 
            print ("You cannot withdraw more than what you have in your account")
            raise AbortTransaction ("Amount cannot be more than the current balanace")
        
        self.__prev_balance = self.balance
        self.balance = self.balance - amount_to_withdraw
        self.__show('withdraw')
        return self.balance

    def getBalance (self, password):

        if password != self.password:
            print ("Invalid Password")
            return None
        self.__prev_balance = self.balance
        self.__show('get balance')
        return self.balance 

    def __show(self, label):
        print ()
        print ('Operation Name', label)
        print ("\t\t\t Name: ", self.name)
        print ("\t\t\t Previous Balance: ", self.prev_balance)
        print ("\t\t\t Current Balance: ", self.balance)
        print ("\t\t\t Password: ", self.password)

    def _show(self): 
        print () 
        print ("\t\t\t Name: ", self.name)
        print ("\t\t\t Previous Balance: ", self.prev_balance)
        print ("\t\t\t Current Balance: ", self.balance)
        print ("\t\t\t Password: ", self.password)        


if __name__ == "__main__":
    
    account_1 = Accounts("Rohit", 1000000, 'apple')
    account_1.deposit(893234, 'apple')
    account_1.withdraw(12345, 'apple')
    account_1.getBalance('apple')
    
    account_1.withdraw(1500, 'apple')
