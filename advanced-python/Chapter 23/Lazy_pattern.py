""" 
In some application we want to perform important actions before accessing the object. This where proxy pattern comes in
Before we can access sensitive data; we would like to see if user has sufficient privildeges or not 
Not just sensitive data, proxy pattern can be used in deferring the resource intensive object creation; it will instantiate when user first time uses it 
Idea behind proxy pattern is to help woth performing cretain actions before object is accesssed. 

4 well known proxy types - 
a. Remote Proxy - acts as local representation of an object that exists in different address space e.g. N/w server 
b. Virutal Proxy - Defer object creaton until is needed
c. Protection/Protective Proxy - Control access of sensitive data 
d. Smart (Reference) Proxy - Performs extra action where object is accessed. Actions include reference counting and threadsafety cehcks 
"""

class LazyProperty:
    def __init__(self, method):
        self.method=method
        self.method_name=method.__name__
        # print(f"function overriden: {self.fget}")
        # print(f"function's name: {self.func_name}")

    def __get__(self, obj, cls):
        if not obj:
            return None 
        value=self.method(obj)
        # print(f"value {value}")
        setattr(obj, self.method_name, value)
        return value 
    
class Test:
    def __init__(self):
        self.x = "foo"
        self.y = "bar"
        self._resource=None 

    @LazyProperty
    def resource(self):
        print(f"Initializing self._resource which is {self._resource}")
        self._resource=tuple(range(5))
        return self._resource
    
def main():
    t=Test()
    print(t.x)
    print(t.y)
    print(t.resource)
    print(t.resource)

if __name__=="__main__":
    main()