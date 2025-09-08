""" 
In MVC there are 3 components: Model, View and Controller 
Model is smart; it contains all business logic, data and state. This is the brain of the application 
View is thin: It is the usually the front end of the system 
Controller is dumb: It takes input from View and passes to Model for processing. Acts as link between model and view

Django works on MVC pattern. Only naming convention is little different, controller in Django is called view and view is called template making it MTV pattern 
there are other variations of MVC pattern like Model View Presentor, or Model View Adapter 

"""

quotes=(
    'A man is not complete until he is married. Then he is finished.', 
    'As I said before, I never repeat myself.', 
    'Behind a successful man is an exhausted woman.', 
    'Black holes really suck...',
    'Facts are stubborn things.'
)

""" Model """
class QuoteModel:
    def get_quote(self, n):
        try:
            value=quotes[n]
        except IndexError as ix:
            value="Not Found"
        return value 

""" View """
class QuoteTerminalView:
    def show(self, quote):
        print(f"And the Quote is: {quote}")
    def error(self, msg):
        print(f"Error: {msg}")
    def select_quote(self):
        return input("Which quote quote number you would like to see: ")
    
""" Controller """
class QuoteTerminalController:
    def __init__(self):
        self.model=QuoteModel()
        self.view=QuoteTerminalView()

    def run(self):
        valid_input=False 
        while not valid_input:
            try:
                n=self.view.select_quote()
                n=int(n)
                valid_input=True 
            except ValueError as ve:
                self.view.error(f"Incorrect index: {n}")
        quote=self.model.get_quote(n)
        self.view.show(quote)

def main(): 
    controller=QuoteTerminalController()
    while True:
        controller.run()

if __name__=="__main__":
    main()