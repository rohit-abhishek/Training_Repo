class DimmerSwitch:
    def __init__(self, label):
        self.label = label
        self.switchIsOn = False 
        self.brightness = 0 

    def turnOn(self):
        self.switchIsOn = True 

    def turnOff(self):
        self.switchIsOn = False 
    
    def raiseLevel(self):
        if self.brightness < 10 :
            self.brightness += 1
    
    def lowerLevel(self):
        if self.brightness > 0: 
            self.brightness -= 1
    
    def show(self):
        print()
        print ("Switch is         ", self.label)
        print ("Switch is on?     ", self.switchIsOn)
        print ("Switch Brightness ", self.brightness)

oDimmer_1 = DimmerSwitch("Wipro") 
oDimmer_1.turnOn()
oDimmer_1.raiseLevel()
oDimmer_1.raiseLevel()
oDimmer_1.raiseLevel()
oDimmer_1.raiseLevel()
oDimmer_1.show()


oDimmer_2 = DimmerSwitch("Samsung") 
oDimmer_2.turnOn()
oDimmer_2.raiseLevel()
# oDimmer_2.lowerLevel()
oDimmer_2.turnOff()
oDimmer_2.show()