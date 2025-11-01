class Stack:
    def __init__(self, startingStackAsList=None) -> None:

        # initialize datalist if startingStackLiost is empty otherwise copy the content
        if startingStackAsList is None:
            self.dataList = [] 
        else: 
            self.dataList = startingStackAsList[:]

    def push(self, item):
        self.dataList.append(item)

    def pop(self):
        if len(self.dataList) == 0: 
            raise IndexError
        element = self.dataList.pop()
        return element
    
    def peek(self):
        item = self.dataList[-1]
        return item 
    
    def getSize(self):
        n_elements = len(self.dataList)
        return n_elements
    
    def show(self):
        print ("Stack is ")
        for i in reversed(self.dataList):
            print ("    ", i)


stack = Stack([1,2,3,4])            
stack.show()
stack.pop()
stack.peek()
stack.push(5)
stack.show()