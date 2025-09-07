""" 
Unlike apple factory we can also opt for assembled computers. The apple factory on one hand creates preconfigured mac-mini 
this will use builder pattern to create custom computer based on client need 
"""

import random
import string 

def random_string_generator(length=8):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

class Computer:
    def __init__(self, serial_number):
        self.serial=serial_number
        self.memory=None 
        self.hdd=None 
        self.gpu=None 
    def __str__(self):
        info=(f"Model:  {self.serial}", f"Memory:    {self.memory} GB", f"Hard Disk:  {self.hdd} GB", f"Graphics Processor:    {self.gpu}")
        return "\n".join(info)
    
class Tablet:
    def __init__(self, serial_number):
        self.serial=serial_number
        self.memory=None 
        self.hdd=None 
        self.size=None 
    def __str__(self):
        info=(f"Model:  {self.serial}", f"Memory:    {self.memory} GB", f"Hard Disk:  {self.hdd} GB", f"Size:    {self.size} inches")
        return "\n".join(info)
    

# Computer builder class - This is our Builder module 
class ComputerBuilder:
    def __init__(self):
        self.computer=Computer(random_string_generator(8))
    def configure_memory(self, memory):
        self.computer.memory = memory
    def configure_hdd(self, hdd):
        self.computer.hdd=hdd
    def configure_gpu(self, gpu):
        self.computer.gpu=gpu 

class TabletBuilder:
    def __init__(self):
        self.computer=Tablet(random_string_generator(5))
    def configure_memory(self, memory):
        self.computer.memory = memory
    def configure_hdd(self, hdd):
        self.computer.hdd=hdd
    def configure_size(self, size):
        self.computer.size=size     


# Hardware engineer class - this is our director module 
class HardwareEngineer:
    def __init__(self):
        self.builder=None 
    
    def construct_computer(self, memory, hdd, gpu):
        self.builder=ComputerBuilder()
        steps=(self.builder.configure_memory(memory), self.builder.configure_hdd(hdd), self.builder.configure_gpu(gpu))
        [step for step in steps]

    def construct_tablet(self, memory, hdd, size):
        self.builder=TabletBuilder()
        steps=(self.builder.configure_memory(memory), self.builder.configure_hdd(hdd), self.builder.configure_size(size))
        [step for step in steps]

    @property
    def computer(self):
        return self.builder.computer


# main class 
def main():
    engineer=HardwareEngineer()
    computer_type=input("Enter C for computer and T for Table: ")
    if computer_type.strip().upper()=="C":
        engineer.construct_computer(memory=8, hdd=1, gpu="Nvidia RTX")
    elif computer_type.strip().upper()=="T":
        engineer.construct_tablet(memory=4, hdd=500, size=10)
    else: 
        raise ValueError(f"I dont know how to make computer {computer_type}. Please try again")
    
    computer=engineer.computer
    print(computer)

if __name__=="__main__":
    main()