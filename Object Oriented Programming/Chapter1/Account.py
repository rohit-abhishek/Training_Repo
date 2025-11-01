class Account:

    def __init__(self, name, balance, password):
        self.name = name
        self.balance = balance 
        self.password = password 

    def deposit(self, amount_to_deposit, password):

        if password != self.password:
            print ("Invalid Password")
            return None 
        
        if amount_to_deposit < 0: 
            print("You cannot deposit negative amount")
            return None 
        
        self.balance = self.balance + amount_to_deposit

        return self.balance 
    
    def withdraw(self, amount_to_withdraw, password): 

        if password != self.password:
            print ("Invalid Password")
            return None

        if amount_to_withdraw < 0: 
            print ("You cannot withdraw negative amount")
            return None 

        self.balance = self.balance - amount_to_withdraw

        return self.balance

    def getBalance (self, password):

        if password != self.password:
            print ("Invalid Password")
            return None

        return self.balance 

    def show(self):
        print ("\t\t\t Name: ", self.name)
        print ("\t\t\t Balance: ", self.balance)
        print ("\t\t\t Password: ", self.password)


if __name__ == "__main__":
    
    account_1 = Account('Rohit', 1000000, 'Apple')
    if account_1.deposit(50000, 'apple'):
        account_1.show()
