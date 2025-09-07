"""
this pattern is useful when we want to create object which is clone of another object.  
"""

import copy 

class Website:
    """ This class will hold website information, some paramters are defined in init() method and some are passed in kwargs in form of key=value pair"""
    def __init__(self, name, domain, description, author, **kwargs):
        self.name=name
        self.domain=domain 
        self.description=description
        self.author=author 

        # sets the name of the attribute 
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        summary=[f"Website: {self.name}\n"]

        # get the information of the object 
        informations=vars(self).items() 
        ordered_informations=sorted(informations)

        for attr, val in ordered_informations:
            if attr == "name":
                continue
            summary.append(f"{attr} : {val}")

        return " ".join(summary)
    

class Prototype:
    def __init__(self):
        self.objects = dict() 
    
    def register(self, identifier, obj):
        self.objects[identifier] = obj

    def unregister(self, identifier):
        del self.objects[identifier]
    
    def clone(self, identifier, **attrs):
        found=self.objects.get(identifier)

        if not found:
            raise ValueError(f"Incorrect object identifier {identifier}")
        
        obj=copy.deepcopy(found)

        for key in attrs:
            setattr(obj, key, attrs[key])
        
        return obj
    

def main():
    keywords=["python", "data", "apis", "automation"]
    site_1=Website("ContentGardening", domain="contentgardening.com", description="Automation and data driven apps", author="Kamon Aveya", category="Blog", keywords=keywords)
    prototype=Prototype()
    identifier="ABCDEFGH"
    prototype.register(identifier, site_1)

    site_2=prototype.clone(identifier, name="ContentGardeningPlayground", domain="playground.contentgardening.com", description="Experimentation techniques for blog", category="Membership site", creation_date="2008-01-01")

    # lets compare the objects 
    for site in (site_1, site_2):
        print("printing object by calling str method")
        print(site)
        print ("Category: ", site.category)
        print()


    print(f"ID of site_1: {id(site_1)}")
    print(f"ID of site_2: {id(site_2)}")

if __name__=="__main__":
    main()