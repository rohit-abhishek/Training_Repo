class Publisher:
    def __init__(self):    
        self.observers=[] 
    
    def add(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print (f"Failed to add observer {observer}")

    def remove(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError as ve:
            print (f"Failed to remove observer {observer}")

    def notify(self):
        [o.notify(self) for o in self.observers]

class DefaultFormatter(Publisher):
    def __init__(self, name):
        Publisher.__init__(self)
        self.name=name 
        self._data=0 
    
    def __str__(self):
        return f"{type(self).__name__}:{self.name} has data={self._data}"
    
    @property
    def data(self):
        return self._data 
    
    @data.setter 
    def data(self, new_value):
        try:
            self._data=int(new_value)
        except ValueError as e:
            print (f"Error: {str(e)}")
        else:
            self.notify()


class HexFormatterObs:
    def notify(self, publisher):
        value=hex(publisher.data)
        print(f"{type(self).__name__}:{publisher.name} has now hex data={value}")

class BinaryFormatterObs:
    def notify(self, publisher):
        value=bin(publisher.data)
        print(f"{type(self).__name__}:{publisher.name} has now bin data={value}")

def main():
    default_formatter=DefaultFormatter("test1")
    print(default_formatter)
    print() 

    hex_formatter=HexFormatterObs()
    default_formatter.add(hex_formatter)
    default_formatter.data=3
    print(default_formatter)
    print()

    binary_formatter=BinaryFormatterObs() 
    default_formatter.add(binary_formatter)
    default_formatter.data=21
    print(default_formatter)
    print() 

    # removing observer should not crash
    default_formatter.remove(hex_formatter)
    default_formatter.data=40 
    print(default_formatter)
    print() 

    default_formatter.remove(hex_formatter)
    default_formatter.add(binary_formatter)
    default_formatter.data="hello"
    print(default_formatter)
    print() 

    default_formatter.data=15.8 
    print(default_formatter)        


if __name__=="__main__":
    main()