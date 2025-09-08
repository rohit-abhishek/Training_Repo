import abc 
import urllib.request, urllib.parse

class ResourceContent:
    """ Defines the abstraction interface. maintains a reference of object that is called implementor"""

    def __init__(self, imp):
        self._imp=imp 

    def show_content(self, path):
        self._imp.fetch(path)


class ResourceContentFetcher(metaclass=abc.ABCMeta):
    """ define the interface for implementaion class that fetch the content """

    @abc.abstractmethod
    def fetch(path):
        pass 


class URLFetcher(ResourceContentFetcher):
    """ Implements the implementor interface and defines it concrete implementation """

    def fetch(self, path):
        req=urllib.request.Request(path)
        with urllib.request.urlopen(req) as response:
            if response.code==200:
                the_page=response.read()
                print(the_page)

class LocalFileFetcher(ResourceContentFetcher):
    """ Implements the implementor interface and defines it concrete implementation """

    def fetch(self, path):
        with open(path) as f:
            print (f.read())


def main():
    url_fetcher=URLFetcher()
    iface=ResourceContent(url_fetcher)
    iface.show_content("https://google.com")

    print ("=================================")

    local_file_fetcher=LocalFileFetcher()
    iface=ResourceContent(local_file_fetcher)
    iface.show_content("advanced-python/Chapter 21/file.txt")


if __name__=="__main__":
    main()