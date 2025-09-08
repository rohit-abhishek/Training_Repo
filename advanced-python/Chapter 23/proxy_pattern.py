""" Here we will implement proxy pattern for restricting access 
services provided are  list all users and adding new user 
"""

class SensitiveInfo:
    def __init__(self):
        self.users=["nick", "tom", "ben", "mike"]

    def read(self):
        nb=len(self.users)
        print(f"There are {nb} users: {' '.join(self.users)}")
    
    def add(self, user):
        self.users.append(user)
        print(f"Added User: {user}")


""" Info class is protection proxy of SensitiveInfo"""
class Info:
    """ Protection Proxy """
    def __init__(self):
        self.protected=SensitiveInfo() 
        self.secret="0xdeadbeef"
    
    def read(self):
        self.protected.read()

    def add(self, user):
        sec=input("What is the secret?: ")
        self.protected.add(user) if sec==self.secret else print("That's wrong")

def main():
    info = Info()
    while True:
        print('1. read list |==| 2. add user |==| 3. quit') 
        key=input("Choose Option: ")
        if key=="1":
            info.read()
        elif key== "2":
            name=input("Choose name: ")
            info.add(name)
        elif key=="3":
            exit()
        else:
            print(f"Unknown option: {key}")

if __name__=="__main__":
    main()