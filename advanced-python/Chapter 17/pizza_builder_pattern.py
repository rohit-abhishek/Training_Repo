from enum import Enum
import time 


PizzaProgress=Enum("PizzaProgress", "queued preparation baking ready")
PizzaDough=Enum("PizzaDough", "thin thick")
PizzaSauce=Enum("PizzaSauce", "tomato creme_fraiche")
PizzaTopping=Enum("PizzaTopping", "mozzarella double_mozzarella bacon ham mushroom red_onion oregano")

STEP_DELAY=3


class Pizza:
    def __init__(self, name):
        self.name=name
        self.dough=None 
        self.sauce=None
        self.topping=[]
    
    def __str__(self):
        return self.name
    
    def prepare_dough(self, dough):
        self.dough=dough
        print (f"Preparing the {self.dough.name} dough of your {self}...")
        time.sleep(STEP_DELAY)
        print (f"Done with the {self.dough.name} dough")


# there are 2 builders - one for creating margeretta pizza and another one creating bacon pizza. Each builder creates Pizza instance
class MargaritaBuilder:
    def __init__(self):
        self.name="margarita"
        self.pizza = Pizza(self.name)
        self.progress=PizzaProgress.queued
        self.baking_time=5 

    def prepare_dough(self):
        self.progress=PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thin)
    
    def add_sauce(self):
        print(f"Adding tomato sauce to your {self.name} pizza")
        self.pizza.sauce=PizzaSauce.tomato
        time.sleep(STEP_DELAY)
        print(f"Done with tomato sauce")

    def add_topping(self):
        print(f"Adding Toppings to your {self.name} pizza")
        topping_desc="double mozarella, oregano"
        topping_items=(PizzaTopping.double_mozzarella, PizzaTopping.oregano)
        print (f"Adding the toppings ({topping_desc}) to your {self.name}")
        self.pizza.topping.append([t for t in topping_items])
        time.sleep(STEP_DELAY)
        print (f"Done with topping {topping_desc}")

    def bake(self):
        self.progress=PizzaProgress.baking
        print(f"Baking your {self.name} pizza for {self.baking_time} seconds")
        time.sleep(self.baking_time)
        self.progress=PizzaProgress.ready
        print(f"Your {self.name} is ready")


class CreamyBaconBuilder:
    def __init__(self):
        self.name="Creamy Bacon"
        self.pizza=Pizza(self.name)
        self.progress=PizzaProgress.queued
        self.baking_time=7

    def prepare_dough(self):
        self.progress=PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thick)
    
    def add_sauce(self):
        print(f"Adding creme fraiche sauce to your {self.name} pizza")
        self.pizza.sauce=PizzaSauce.creme_fraiche
        time.sleep(STEP_DELAY)
        print(f"Done with creme fraiche sauce")

    def add_topping(self):
        print(f"Adding Toppings to your {self.name} pizza")
        topping_desc="mozarella, bacon, ham, mushroom, red onion, oregano"
        topping_items=(PizzaTopping.mozzarella, PizzaTopping.bacon, PizzaTopping.ham, PizzaTopping.mushroom, PizzaTopping.red_onion, PizzaTopping.oregano)
        print (f"Adding the toppings ({topping_desc}) to your {self.name}")
        self.pizza.topping.append([t for t in topping_items])
        time.sleep(STEP_DELAY)
        print (f"Done with topping {topping_desc}")

    def bake(self):
        self.progress=PizzaProgress.baking
        print(f"Baking your {self.name} pizza for {self.baking_time} seconds")
        time.sleep(self.baking_time)
        self.progress=PizzaProgress.ready
        print(f"Your {self.name} is ready")


# Waiter is our director class 
class Waiter:
    def __init__(self):
        self.builder=None 

    def construct_pizza(self, builder):
        self.builder=builder
        steps=(builder.prepare_dough, builder.add_sauce, builder.add_topping, builder.bake)
        [step() for step in steps]

    @property
    def pizza(self):
        return self.builder.pizza
    

def variety_style(builders):
    try:
        input_msg="What pizza would you like (M)aragarita or (C)reamy Beacon: "
        pizza_style=input(input_msg)
        builder=builders[pizza_style.lower()]()
    except:
        print (f"Only Margarita or Creamy Bacon available. Try again")
        return False, None 
    
    return True, builder 


def main():
    builders = dict(m=MargaritaBuilder, c=CreamyBaconBuilder)
    valid_input=False 
    while not valid_input:
        valid_input, builder=variety_style(builders)
    print ()
    
    waiter=Waiter()
    waiter.construct_pizza(builder)
    pizza=waiter.pizza
    print() 
    print(f"Enjoy your {pizza}")


if __name__ == "__main__":
    main()