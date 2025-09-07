""" 
Implementation of factory pattern. Client will have no idea how is object implemented. 
The pattern will centralize all object creation and tracking at one place. Useful when we want to decouple object creation from 
object usage
"""

import json 
import xml.etree.ElementTree as etree 

class JSONDataExtractor:
    def __init__(self, file_path):
        self.data = dict()
        with open(file_path, "r") as fp:
            self.data=json.load(fp)

    @property
    def parsed_data(self):
        return self.data 
        

class XMLDataExtractor:
    def __init__(self, file_path):
        self.tree=etree.parse(file_path)

    @property
    def parsed_data(self):
        return self.tree 
    

def data_extraction_factory(file_path):
    """ factory method to call specific class based on file extension """

    if file_path.endswith("json"): 
        extractor=JSONDataExtractor
    elif file_path.endswith("xml"):
        extractor=XMLDataExtractor
    else:
        raise ValueError(f"Cannot extract data from {file_path}")
    
    return extractor(file_path)


def extract_data(file_path):
    """ Wrapper method for data_extraction_factory """

    file_object=None 
    try:
        file_object=data_extraction_factory(file_path)
    except Exception as e:
        print (e)
    return file_object


def main():
    print ("Below will give error")
    sqlite_factory=extract_data('data/person.sq3')
    print() 

    print("Below will create JSON object")
    json_factory=extract_data('advanced-python/Chapter 16/data/movies.json')
    json_data=json_factory.parsed_data
    for movie in json_data:
        print("Title", movie["title"])
        print("Year", movie["year"])
        print("Direcor", movie["director"])
        print()
    print() 

    print("Below will create XML object")
    xml_factory=extract_data('advanced-python/Chapter 16/data/person.xml')
    xml_data=xml_factory.parsed_data
    liars=xml_data.findall(f".//person[lastName='Liar']")
    for person in liars:
        print("First Name", person.find("firstName").text)
        print("Last Name", person.find("lastName").text)
        print()

if __name__=="__main__":
    main()