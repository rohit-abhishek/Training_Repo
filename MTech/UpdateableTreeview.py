from tkinter import ttk
from tkinter import *

root = Tk()  # initial box declaration
columns = ("name", "IP address")
treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)

# indicates column, not displayed
treeview.column("name", width=100, anchor='center')
treeview.column("IP address", width=300, anchor='center')

treeview.heading("name", text="name")  # Show header
treeview.heading("IP address", text="IP address")

treeview.pack(side=LEFT, fill=BOTH)

name = ['computer 1', 'server', 'notebook']
ipcode = ['10.13.71.223', '10.25.61.186', '10.25.11.163']

for i in range(min(len(name), len(ipcode))):  # write data
    treeview.insert('', i, values=(name[i], ipcode[i]))

def treeview_sort_column(tv, col, reverse):  # treeview, column name, arrangement
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)  # Sort by
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):  # based on sorted index movement
        tv.move(k, '', index)
    
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse)) # Rewrite the title to make it the title of the reverse order
 
def set_cell_value(event): # Double click to enter the edit state
    for item in treeview.selection():
        #item = I001
        item_text = treeview.item(item, "values")
                 #print(item_text[0:2]) # Output the value of the selected row
        column= treeview.identify_column(event.x)# column
        row = treeview.identify_row(event.y) #row

    cn = int(str(column).replace('#',''))
    rn = int(str(row).replace('I',''))

    entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    def saveedit():
        treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        entryedit.destroy()
        okb.destroy()
    okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    okb.place(x=90+(cn-1)*242,y=2+rn*20)
 
def newrow():
    name.append('to be named')
    ipcode.append('IP')
    treeview.insert('', len(name)-1, values=(name[len(name)-1], ipcode[len(name)-1]))
    treeview.update()
    newb.place(x=120, y=(len(name)-1)*20+45)
    newb.update()
 
treeview.bind('<Double-1>', set_cell_value) # Double-click the left button to enter the edit
newb = ttk.Button(root, text='new contact', width=20, command=newrow)
newb.place(x=120,y=(len(name)-1)*20+45)
 
 
for col in columns: # bind function to make the header sortable
    treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
'''
 1. Traversing the table
t = treeview.get_children()
for i in t:
    print(treeview.item(i,'values'))
 2. Bind Click to leave event
 Def treeviewClick(event): #click
    for item in tree.selection():
        item_text = tree.item(item, "values")
                 Print(item_text[0:2]) # Output the value of the first column of the selected row
tree.bind('<ButtonRelease-1>', treeviewClick)  
------------------------------
 Left mouse click click 1/Button-1/ButtonPress-1
 Left mouse click to release ButtonRelease-1
 Right mouse click 3
 Double click on the Double-1/Double-Button-1
 Right click on Double-3
 Mouse wheel click 2
 Mouse wheel double click on Double-2
 Mouse movement B1-Motion
 Mouse moves to area Enter
 Mouse leaves area Leave
 Get keyboard focus FocusIn
 Lose keyboard focus FocusOut
 Keyboard event key
 Enter key Return
 Control size changes to Configure
------------------------------
'''
 
root.mainloop() # enter the message loop
