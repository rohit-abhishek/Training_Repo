import os 
verbose=True 


class RenameFile:
    def __init__(self, src, dest):
        self.src=src 
        self.dest=dest

    def execute(self):
        if verbose:
            print(f"renaming {self.src} to {self.dest}")

        os.rename(self.src, self.dest)

    def undo(self):
        if verbose:
            print(f"renaming {self.dest} back to {self.src}")

        os.rename(self.dest, self.src)


class CreateFile:
    def __init__(self, path, text="Hello World"):
        self.path=path
        self.text=text 

    def execute(self):
        if verbose:
            print(f"creating file {self.path}")

        with open(self.path, "w", encoding="utf-8") as fp:
            fp.write(self.text)

    def undo(self):
        delete_file(self.path)

class ReadFile:
    def __init__(self, path):
        self.path=path 

    def execute(self):
        if verbose:
            print(f"reading file {self.path}")

        with open(self.path, "r", encoding="utf-8") as fp:
            print(fp.read(), end="")

""" implementing deleting file as method instead of class """
def delete_file(path):
    if verbose:
        print(f"deleting file {path}")

    os.remove(path)

def main():
    orig_name, new_name = "advanced-python/Chapter 25/file1", "advanced-python/Chapter 25/file2"

    commands=(CreateFile(orig_name), ReadFile(orig_name), RenameFile(orig_name, new_name))

    [c.execute() for c in commands]

    answer=input("reverse the executed commands (y/n): ")
    if answer.lower().strip() != "y":
        print(f"result is {new_name}")
        exit() 
    
    for c in reversed(commands):
        try:
            c.undo() 
        except Exception as e: 
            print (f"error {e}")

if __name__=="__main__":
    main()