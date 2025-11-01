process_list=[]
blocked_process_id=0

class Process:
  def __init__(self):
    self.id = 0
    self.wait = False
    self.dependents = []
    self.num = 0
    self.parents=[]

def SendReply(from_process, to_process):
    if to_process.wait == True:
        to_process.num = to_process.num -1
        if to_process.num == 0:
            if blocked_process_id == to_process.id:
                print("DEADLOCK OCCURED")
            else:
                for i in to_process.parents:
                    parent_process = process_list[i-1]
                    SendReply(to_process, parent_process)


def SendQuery(from_process):
    if from_process.wait is False :
        from_process.wait = True
        from_process.num = len(from_process.dependents)
        for i in from_process.dependents:
            dependent_process = process_list[i-1]
            if dependent_process.wait == True:
                SendReply(dependent_process, from_process)
            else:
                SendQuery(dependent_process)


def main():
    print("Enter number of processes")
    
    num_of_process = int(input())

    #create process list
    i=1
    while i<=num_of_process:
        temp = Process()
        temp.id = i
        process_list.append(temp)
        i+=1


    print("Enter dependent process,if  multiple process separate by space (Ex: 2 3). If no dependents available enter 0.")
    for process in process_list:
        print("Enter dependent process of - P"+str(process.id))
        dependent_set_input = input()
        if type(dependent_set_input) is str:
            dependent_set_in = dependent_set_input.split()
            for dependentw in dependent_set_in:
               dependent = int(dependentw)
               if dependent > 0:
                 process.dependents.append(dependent)
                 process_list[dependent-1].parents.append(process.id)
        else:
            dependent = int(dependent_set_input)
            if dependent > 0:
                process.dependents.append(dependent)
                process_list[dependent-1].parents.append(process.id)
        

    print("Enter the blocked process Id")
    global blocked_process_id
    blocked_process_id = int(input())
    
    if blocked_process_id > 0:
        blocked_process = process_list[blocked_process_id-1]
        SendQuery(blocked_process)
    else:
        print("Invalid Blocked Process Id")
    print("End")


main()