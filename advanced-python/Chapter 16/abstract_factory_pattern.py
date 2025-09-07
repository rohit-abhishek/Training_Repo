"""
Abstract factory is more generalized form for Factory Design pattern. If there are more factory methods, abstract factory pattern
can be leveraged to create objects. 
The example below is game which takes input whether player is a kid or adult. And then launches the game based on the input
"""

""" Kids Game """

class Frog:
    def __init__(self, name):
        self.name=name
    def __str__(self):
        return self.name
    def interact_with(self, obstacle):
        act = obstacle.action()
        msg=f"{self} the frog encounters obstacle {obstacle} and action {act}"
        print(msg) 

class Bug: 
    def __str__(self):
        return "a bug" 
    def action(self):
        return "eat it"

class FrogWorld:
    def __init__(self, name):
        print(self)
        self.player_name=name 
    def __str__(self):
        return "\n\n\t-------------- Frog World -----------------"   
    def make_character(self):
        return Frog(self.player_name)
    def make_obstacle(self):
        return Bug()
    
""" Adults Game """
class Wizard:
    def __init__(self, name):
        self.name=name
    def __str__(self):
        return self.name 
    def interact_with(self, obstacle):
        act=obstacle.action() 
        msg=f"{self} Wizard battles {obstacle} and action {act}"
        print (msg)

class Ork:
    def __str__(self):
        return "an evil ork"
    def action(self):
        return "kills it"
    
class WizardWorld:
    def __init__(self, name):
        print(self)
        self.player_name=name
    def __str__(self):
        return "\n\n\t-------------- Wizard World -----------------" 
    def make_character(self):
        return Wizard(self.player_name)
    def make_obstacle(self):
        return Ork() 

""" Entry point for game """
class GameEnvironment:
    def __init__(self, factory):
        self.hero = factory.make_character()
        self.obstacle=factory.make_obstacle() 
    def play(self):
        self.hero.interact_with(self.obstacle)


def validate_age(name):
    try:
        age=input(f"Welcome {name}. Enter your age: ")
        age=int(age)
    except ValueError as v:
        print ("Age is invalid, please try again")
        return False, age
    return True, age


def main():
    name = input("Hello, enter your name: ")
    valid_input=False 
    while not valid_input:
        valid_input, age=validate_age(name)
    
    game=FrogWorld if age < 18 else WizardWorld
    environment=GameEnvironment(game(name))
    environment.play() 

if __name__ == "__main__":
    main()

