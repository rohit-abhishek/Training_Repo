"""
Factory pattern returns the object in single go. However, builder pattern creates object in mutliple steps and requires explicit 
call to return the object. 
Consider like buying computer from Apple -> This uses factory pattern, all h/w components are preconfigured and returned back to user 
in single shot 
"""

# notice the sub class MacMini within AppleFactory. This is a neat way to avoid direct instantiation of a class x``

MINI14="Mac Mini 1.4 GHz"
class AppleFactory:
    class MacMini14:
        def __init__(self):
            self.memory=4
            self.hdd=500
            self.gpu="Integrated"
        def __str__(self):
            info=(f"Model:  {MINI14}", f"Memory:    {self.memory}", f"Hard Disk:  {self.hdd}", f"Graphics Processor:    {self.gpu}")
            return "\n".join(info)

    def build_computer(self, model):
        if model==MINI14:
            return self.MacMini14() 
        else:
            return f"I dont know how to build the model {model}"


if __name__ == "__main__":
    afac=AppleFactory()
    mac_mini=afac.build_computer(MINI14)
    print (mac_mini)