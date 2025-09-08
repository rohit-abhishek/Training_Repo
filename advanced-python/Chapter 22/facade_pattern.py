from enum import Enum
from abc import ABC, ABCMeta, abstractmethod

State=Enum("State", "new running sleeping restart zombie")

class Server(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name 
    
    @abstractmethod
    def boot(self):
        pass 

    @abstractmethod
    def kill(self, restart=True):
        pass 

"""A modular OS can have a great number of interesting servers: 
a file server, a process server, an authentication server, a network server, a graphical/window server, and so forth. 
The following example includes two stub servers: FileServer and ProcessServer."""

class FileServer(Server):
    def __init__(self):
        """ Action required for initializing the file server """
        self.name="FileServer"
        self.state=State.new 
    
    def boot(self):
        """ action required for booting the server """
        print (f"booting the {self}")
        self.state=State.running

    def kill(self, restart=True):
        """ action required for killing the server """
        self.state=State.restart if restart else State.zombie
    
    def create_file(self, user, name, permissions):
        """ check validity of permission, user rights etc """
        print (f"Trying to create file {name} for user {user} with permissions {permissions}")


class ProcessServer(Server):
    def __init__(self):
        """ Action required for initializing the file server """
        self.name="ProcessServer"
        self.state=State.new 

    def boot(self):
        """ actions required for booting the process server """
        print(f"Booting the {self}")
        self.state=State.running

    def kill(self, restart=True):
        """ action reqiured for killing the process server """
        self.state=State.restart if restart else State.zombie

    def creatre_process(self, user, name):
        """ check user rights, generated PID etc """
        print(f"Trying to create process server {name} for user {user}")

""" Operating system class is facade. In its __init__ method all the server instances are created.. start() in client code 
is the entry point to the system. more wrappers can be added to aceess points to the services of the server such as create_file and create_process"""

class OperatingSsytem:
    """ The Facade """

    def __init__(self):
        self.fs=FileServer() 
        self.ps=ProcessServer()

    def start(self):
        [i.boot() for  i in (self.fs, self.ps)]
    
    def create_file(self, user, name, permissions):
        return self.fs.create_file(user, name, permissions)
    
    def create_process(self, user, name):
        return self.ps.creatre_process(user, name)
    

def main():
    os=OperatingSsytem() 
    os.start() 
    os.create_file("foo", "hello", "-rw-r-r")
    os.create_process("bar", "ls/tmp")

if __name__=="__main__":
    main()