"""
Adapter pattern is when we want to make two incompatble interface compatible 
"""

class Club:
    def __init__(self, name):
        self.name=name 

    def __str__(self):
        return f"the club {self.name}"
    
    def organize_event(self):
        return "hire an artist to perform for people"
    

# we have musician and dancer class one with play method and another with dance method 
class Musician:
    def __init__(self, name):
        self.name=name 
    def __str__(self):
        return f"the musician {self.name}"
    def play(self):
        return "plays music"
    
class Dancer:
    def __init__(self, name):
        self.name=name
    def __str__(self):
        return f"the dancer {self.name}"
    def dance(self):
        return "does a dance performance"
    

# client code only knows about organize performance; does not know about dance and play. So we will use adapter method 
class Adapter:
    def __init__(self, obj, adapted_methods):
        self.obj=obj
        self.__dict__.update(adapted_methods)
    def __str__(self):
        return str(self.obj)
    
def main():
    objects = [Club("New Rock"), Musician("Hans Zimmer"), Dancer("Shane Sparks")]

    for obj in objects:
        if hasattr(obj, "play") or hasattr(obj, "dance"):
            if hasattr(obj, "play"):
                adapted_methods=dict(organize_event=obj.play)
            elif hasattr(obj, "dance"):
                adapted_methods=dict(organize_event=obj.dance)

            obj=Adapter(obj, adapted_methods)

        print (f"{obj} {obj.organize_event()}" )

if __name__ == "__main__":
    main()