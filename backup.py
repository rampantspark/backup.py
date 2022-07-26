from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as msg
import json

class MainApplication(Tk):

    tree = None
    location_count = 0
    btnEditSchedule = None
    btnEditScheduleEdit = None
    cmbSelected = None
    cmbSelectedEdit = None
      
    def __init__(self):
        super().__init__()
        
        self.title("backup.py")
        self.geometry("750x500")
        self.resizable(False, False)
        #self.iconphoto(False, PhotoImage(file="assets/title_icon.png"))
        
        global tree
        # MAIN WINDOW GUI
        columns = ('id', 'name', 'source', 'destination', 'schedule', 'last_backup', 'next_backup', 'status')
        # Define Title Label
        lblTitle = Label(self, text="Backup.py", font=("Arial", 25))
        # Define Tree View Frame
        frame = Frame(self)
        # Define Tree View
        tree = Treeview(frame, columns=columns, show="headings")

        tree.heading('id', text="ID")
        tree.column('id', minwidth=30, width=30, stretch=False)
        tree.heading('name', text="Name")
        tree.column('name', minwidth=90, width=90, stretch=False)
        tree.heading('source', text="Source")
        tree.column('source', minwidth=120, width=120, stretch=False)
        tree.heading('destination', text="Destination")
        tree.column('destination', minwidth=120, width=120, stretch=False)
        tree.heading('schedule', text="Schedule")
        tree.column('schedule', minwidth=90, width=90, stretch=False)
        tree.heading('last_backup', text="Last Backup")
        tree.column('last_backup', minwidth=90, width=90, stretch=False)
        tree.heading('next_backup', text="Next Backup")
        tree.column('next_backup', minwidth=90, width=90, stretch=False)
        tree.heading('status', text="Status")
        tree.column('status', minwidth=50, width=50, stretch=False)
        # Define Tree View Scrollbar
        scrlTree = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrlTree.set)
        # Main Functionality Buttons
        btnAdd = Button(self, text="Add Source...", command=self.openAddSourceWindow)
        btnEdit = Button(self, text="Edit Source...", command=self.openEditSourceWindow)
        btnDelete = Button(self, text="Remove Source...", command=self.removeSource)
        btnBackup = Button(self, text="Backup Now...")
        # Push Title to Grid
        lblTitle.grid(column=0, row=0, columnspan=4, padx=0, pady=30)
        # Push the Frame, Tree View, and Scrollbar to Grid
        frame.grid(column=0, row=1, columnspan=4, padx=20, pady=20)
        tree.grid(column=0, row=1, columnspan=4, padx=0, pady=0, sticky='nsew')
        scrlTree.grid(column=4, row=1, padx=0, sticky="ns")
        # Populate the Tree with JSON location data
        self.populate_tree(self)
        # Push Main Functionality Buttons to Grid
        btnAdd.grid(column=0, row=4, padx=15, pady=20)
        btnEdit.grid(column=1, row=4, padx=15, pady=20)
        btnDelete.grid(column=2, row=4, padx=15, pady=20)
        btnBackup.grid(column=3, row=4, padx=15, pady=20)
    
    def populate_tree(event, self):
        global tree
        global location_count
        #Read from json file and populate treelist
        with open("locations.json", "r") as file:
            data = json.loads(file.read())
            testDict = {}
            testDict = data

        for d in data:
            tree.insert('', END, values=(d['id'], d['name'], d['source'], d['destination'], d['schedule'], d['lastbackup'], d['nextbackup'], d['status']))
            self.location_count +=1
            print(self.location_count)
    
    def clearTree():
        #clear the tree
        for item in tree.get_children():
                tree.delete(item)
    
    def openAddSourceWindow(self):
        # Toplevel object which will
        # be treated as a new window
        addSourceWindow = Toplevel(self)
        # sets the title of the
        # Toplevel widget
        addSourceWindow.title("Add Source...")
        # sets the geometry of toplevel
        addSourceWindow.geometry("400x300") 
        global btnEditSchedule
        global cmbSelected
        lblName = Label(addSourceWindow, text="Name:")
        txtName = Entry(addSourceWindow)
        lblSource = Label(addSourceWindow, text="Source:")
        txtSource = Entry(addSourceWindow)
        lblDestination = Label(addSourceWindow, text="Destination:")
        txtDestination = Entry(addSourceWindow)
        lblSchedule = Label(addSourceWindow, text="Schedule:")
        cmbSelected = StringVar()
        cmbSchedule = Combobox(addSourceWindow, textvariable= cmbSelected)
        
        cmbSelected.trace('w', self.switchStateAdd)
        cmbSchedule['values'] = ("Never", "Weekly", "Every Two Weeks")
        btnEditSchedule = Button(addSourceWindow, text="Change Schedule", state=DISABLED, command=self.openEditScheduleWindow)
        btnCancel = Button(addSourceWindow, text="Cancel", command=addSourceWindow.destroy)
        btnSubmit = Button(addSourceWindow, text="Okay", command=lambda: self.addSource(txtName.get(), txtSource.get(), txtDestination.get(), cmbSchedule.get(), addSourceWindow))
        lblName.grid(column=0, row=0, padx=50, pady=10)
        txtName.grid(column=1, row=0, padx=10, pady=10)
        lblSource.grid(column=0, row=1, padx=50, pady=10)
        txtSource.grid(column=1, row=1, padx=10, pady=10)
        lblDestination.grid(column=0, row=2, padx=50, pady=10)
        txtDestination.grid(column=1, row=2, padx=10, pady=10)
        lblSchedule.grid(column=0, row=3, padx=50, pady=10)
        cmbSchedule.grid(column=1, row=3, padx=10, pady=10)
        #cmbSchedule.bind('<<ComboboxSelected>>', switchStateAdd)
        #cmbSchedule.current(0)
        btnEditSchedule.grid(column=1, row=4, padx=50, pady=10)
        btnCancel.grid(column=0, row=5)
        btnSubmit.grid(column=1, row=5)
    
        return addSourceWindow

    def switchStateAdd(*arg):
        if cmbSelected.get() == "Never":
            btnEditSchedule["state"] = "disabled"
        else:
            btnEditSchedule["state"] = "normal"

        print("switchStateAdd was run")
 
    def addSource(self, name, source, destination, schedule, window):
        global location_count
        print(name + source + destination)
        # Make sure the data to save exists
        if not name or not source or not destination:
            msg.showwarning("Add Source", "Please make sure all fields are populated...")
        else:
            window.destroy()
            #update counter variable
            new_count = location_count + 1
            # Define JSON Data to save in dictionary
            data = {
                    "id" : new_count,
                    "name" : name,
                    "source" : source,
                    "destination" : destination,
                    "schedule" : schedule,
                    "lastbackup" : "Never",
                    "nextbackup" : "test",
                    "status" : "status"
            }
            # Open and  read from JSON file
            with open("locations.json", "r+") as file:
                # Set file data equal to variable
                location_data = json.load(file)
                #Append new data to file data
                location_data.append(data)
                # Reset iteration to first line
                file.seek(0)
                # Dump data to file
                json.dump(location_data, file, indent=4)

            #clear treeview
            self.clearTree()
            # Reset location count
            location_count = 0
            # Populate the Tree View
            self.opulateTree()
    
    def openEditScheduleWindow(self):
        editScheduleWindow = Toplevel(self)

        # sets the title of the
        # Toplevel widget
        editScheduleWindow.title("Add Source...")

        # sets the geometry of toplevel
        editScheduleWindow.geometry("400x300")
    ####### Edit Source Window #######
    def openEditSourceWindow(self):
        editSourceWindow = Toplevel(self)
        editSourceWindow.title("Edit Source...")
        editSourceWindow.geometry("400x300")
        global btnEditScheduleEdit
        global cmbSelectedEdit
        # Get the currently selected tree view item
        ###### ADD ERROR HANDLING HERE WITH IF STATEMENT
        selected_item = tree.selection()[0]
        temp = tree.item(selected_item)
        # Update values
        id = temp['values'][0]
        name = temp['values'][1]
        source = temp['values'][2]
        destination = temp['values'][3]
        schedule = temp['values'][4]

        current = 0

        if schedule == "Never":
            current=0
        elif schedule == "Weekly":
            current=1
        elif schedule == "Every Two Weeks":
            current=2
        else:
            #throw an exception
            current=3
            
        #cmbSelectedEdit = StringVar()
        #cmbSelectedEditRead = StringVar()
        
        lblName = Label(editSourceWindow, text="Name:")
        txtName = Entry(editSourceWindow)
        txtName.insert(0, name)
        lblSource = Label(editSourceWindow, text="Source:")
        txtSource = Entry(editSourceWindow)
        txtSource.insert(1, source)
        lblDestination = Label(editSourceWindow, text="Destination:")
        txtDestination = Entry(editSourceWindow)
        txtDestination.insert(2, destination)
        lblSchedule = Label(editSourceWindow, text="Schedule:")
        cmbSchedule = Combobox(editSourceWindow)
        
        #cmbSelectedEdit.trace('r', self.switchStateEdit)
        cmbSchedule['values'] = ("Never", "Weekly", "Every Two Weeks")
        cmbSchedule.current(current)
        btnCancel = Button(editSourceWindow, text="Cancel", command=editSourceWindow.destroy)
        btnSubmit = Button(editSourceWindow, text="Add", command=lambda: self.editSource(id, txtName.get(), txtSource.get(), txtDestination.get(), cmbSchedule.get(), editSourceWindow))

        btnEditScheduleEdit = Button(editSourceWindow, text="Change Schedule", state=DISABLED, command=self.openEditScheduleWindow)
        self.readStateEdit(self)
        lblName.grid(column=0, row=0, padx=50, pady=10)
        txtName.grid(column=1, row=0, padx=10, pady=10)
        lblSource.grid(column=0, row=1, padx=50, pady=10)
        txtSource.grid(column=1, row=1, padx=10, pady=10)
        lblDestination.grid(column=0, row=2, padx=50, pady=10)
        txtDestination.grid(column=1, row=2, padx=10, pady=10)
        lblSchedule.grid(column=0, row=3, padx=50, pady=10)
        cmbSchedule.grid(column=1, row=3, padx=10, pady=10)
        cmbSchedule.bind('<<ComboboxSelected>>', self.switchStateEdit)
        
        btnEditScheduleEdit.grid(column=1, row=4, padx=50, pady=10)
        
        btnCancel.grid(column=0, row=5)
        btnSubmit.grid(column=1, row=5)
        
        #return editSourceWindow
    def readStateEdit(event, self):
        print("event")
        print(event.)
        if selfcmbSchedule.get() == "Never":
            btnEditScheduleEdit["state"] = "disabled"
        else:
            btnEditScheduleEdit["state"] = "normal"
    def switchStateEdit(event):
        if cmbSelectedEdit.get() == "Never":
            btnEditScheduleEdit["state"] = "disabled"
        else:
            btnEditScheduleEdit["state"] = "normal"
            
        print("switchStateEdit was run")    
    # Edit Source Logic
    def editSource(self, id, name, source, destination, schedule, window):
        print(name + source + destination)

        if not name or not source or not destination:
            msg.showwarning("Edit Source", "Please make sure all fields are populated...")
        else:
            window.destroy()

            data = {
                    "id" : id,
                    "name" : name,
                    "source" : source,
                    "destination" : destination,
                    "schedule" : schedule,
                    "lastbackup" : "test",
                    "nextbackup" : "test",
                    "status" : "status"
            }

            print(data)

            with open("locations.json", "r") as file:

                lines = json.load(file)

                print(lines)

                for i, obj in enumerate(lines):
                    if obj["id"] == id:
                        #set new data in place of old data
                        #print(obj["name"])
                        obj["name"] = name
                        obj["source"] = source
                        obj["destination"] = destination
                        obj["schedule"] = schedule
                        break

            with open("locations.json", "w") as file:

                file.write(json.dumps(lines, indent=2))

            #clear the treeview
            self.clearTree()
            #populate the treeview
            self.populateTree()
    # Remove Source Logic
    def removeSource(self):
        global location_count
        confirm = msg.askokcancel("Remove Source...", "Are you sure you want to remove this backup location?")

        if confirm:
            reply = "okay"

            # Get selected item to Delete
            selected_item = tree.selection()[0]
            temp = tree.item(selected_item)

            id = temp['values'][0]
            tree.delete(selected_item)

            with open("locations.json", "r") as file:

                    lines = json.load(file)

                    print(lines)

                    for i, obj in enumerate(lines):
                        if obj["id"] == id:
                            print
                            lines.pop(i)
                            break

            with open("locations.json", "w") as file:

                    file.write(json.dumps(lines, indent=2))

            #clear treeview
            self.clearTree(self)

            location_count = 0

            self.populateTree(self)
        else:
            reply = "cancel"
    # Individual Backup Logic
    def backup():
        #Do this
        msg.showwarning("Remove Source...", "Are you sure you want to remove this backup location?")
    # Backup All Logic
    def backupAll():
        msg.showwarning("Remove Source...", "Are you sure you want to remove this backup location?")
 
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()