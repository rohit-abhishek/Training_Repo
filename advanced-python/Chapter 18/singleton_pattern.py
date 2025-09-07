""" 
Implementation of singleton pattern for URL fetcher which will have only one instance running all three urls
"""

import urllib.parse
import urllib.request

class SingletonType(type):
    _instances={} 

    def __call__(cls, *args, **kwds):
        if cls not in cls._instances:
            cls._instances[cls]=super(SingletonType, cls).__call__(*args, **kwds)
        return cls._instances[cls]
    

# we will use metaclass; this acts as blueprint for creating class; just like class is blueprint for object. 
# metaclass is blueprint for generating class 

class URLFetcher(metaclass=SingletonType):
    def __init__(self):
        self.urls=[] 

    def fetch(self, url):
        req=urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            if response.code==200:
                the_page=response.read()
                print(the_page)
                print()

                urls=self.urls
                urls.append(url)
                self.urls=urls

    def dump_url_registry(self):
        return ", ".join(self.urls)
    
def main():
    MY_URLS=[
        "https://google.com",
        "https://python.org", 
        "https://www.python.org/error"
    ]

    print(URLFetcher() is URLFetcher())
    print()

    # create fetcher object 
    fetcher=URLFetcher()
    for url in MY_URLS:
        try:
            fetcher.fetch(url)
        except Exception as e:
            print(e)
        
    print ("-----------------------------")
    done_urls=fetcher.dump_url_registry()
    print(f"Done URLs: {done_urls}")


if __name__=="__main__":
    main()