class Stack:
    def __init__(self, starting_stack_as_list=None) -> None:
        print ('__init__')
        self.data_list = starting_stack_as_list

    @property
    def data_list(self):
        ''' get the stack list '''
        print ()
        print ('getter')
        return self.__data_list
    
    @data_list.setter
    def data_list(self, list_as_stack):
        ''' set data_list item '''
        print ()
        print ('setter')
        if list_as_stack is None:
            self.__data_list = [] 

        else: 
            self.__data_list = list_as_stack[:]

    def push(self, item):
        ''' push element to the top of stack '''
        print ()
        print ('push')
        self.data_list.append(item)

    def pop(self):
        ''' remove the top element '''
        if len(self.data_list) == 0: 
            raise IndexError
        
        element = self.data_list.pop()
        return element

    def peek(self):
        ''' look at the top item without removing it '''
        item = self.data_list[-1]

        return item 
    
    def get_size (self):
        n_elements = len(self.data_list)
        return n_elements

    def show(self):
        print ()
        print ('Stack is ')
        for value in reversed(self.data_list):
            print ('    ', value)

s = Stack([20,19,18])
s.push(10)

# print(s.data_list)