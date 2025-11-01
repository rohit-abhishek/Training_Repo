class Club:
    def __init__(self, club_name, max_member) -> None:
        self.club_name = club_name
        self.max_member = max_member
        self.member_list = [] 

    def addMember(self, name):
        if len(self.member_list) < self.max_member:
            self.member_list.append(name)
            print ("OK..", name, "has been added", self.club_name, "club")

        else: 
            print ("Sorry but we cannot add ", name, "to the ", self.club_name, "club")
            print ("Max number of members reached", self.max_member)

    def report(self):
        print ()
        print ("Here are ", len(self.member_list), "member of the ", self.club_name)
        for name in self.member_list:
            print ("   " ,name)

        print ()