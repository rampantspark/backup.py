from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as msg
import json

# Global vars
tree = None
location_count = 0
btnEditSchedule = None
btnEditScheduleEdit = None
cmbSelected = None
cmbSelectedEdit = None
cmbChangeSchedule = None
cmbTime = None

class MainApplication(Tk):

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
        lblTitle = Label(self, text="backup.py", font=("Arial", 25))
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
        btnBackup = Button(self, text="Backup Selected...")
        btnBackupNow = Button(self, text="Backup All")
        # Push Title to Grid
        lblTitle.grid(column=0, row=0, columnspan=5, padx=0, pady=30)
        # Push the Frame, Tree View, and Scrollbar to Grid
        frame.grid(column=0, row=1, columnspan=5, padx=30, pady=20)
        tree.grid(column=0, row=1, columnspan=5, padx=0, pady=0, sticky='nsew')
        scrlTree.grid(column=6, row=1, padx=0, sticky="ns")
        # Populate the Tree with JSON location data
        self.populate_tree()
        # Push Main Functionality Buttons to Grid
        btnAdd.grid(column=0, row=4, padx=5, pady=20)
        btnEdit.grid(column=1, row=4, padx=5, pady=20)
        btnDelete.grid(column=2, row=4, padx=5, pady=20)
        btnBackup.grid(column=3, row=4, padx=5, pady=20)
        btnBackupNow.grid(column=4, row=4, padx=5, pady=10)

    def populate_tree(event):
        global tree
        global location_count
        #Read from json file and populate treelist
        with open("locations.json", "r") as file:
            data = json.loads(file.read())
            testDict = {}
            testDict = data

        for d in data:
            tree.insert('', END, values=(d['id'], d['name'], d['source'], d['destination'], d['schedule'], d['lastbackup'], d['nextbackup'], d['status']))
            location_count +=1
            print(location_count)

    def clearTree(event):
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
        addSourceWindow.resizable(False, False)

        global cmbSelected
        global cmbSchedule
        global cmbChangeSchedule
        global cmbTime
        
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
        
        lblWeeks = Label(addSourceWindow, text="Day:")
        lblTime = Label(addSourceWindow, text="Time:")
        cmbChangeSchedule = Combobox(addSourceWindow, state=DISABLED)
        cmbChangeSchedule['values'] = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
        cmbChangeSchedule.current(0)
        
        cmbTime = Combobox(addSourceWindow, state=DISABLED)
        cmbTime['values'] = ('00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00')
        cmbTime.current(0)
        
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
        lblWeeks.grid(column=0, row=5, padx=20, pady=10)
        cmbChangeSchedule.grid(column=1, row=5, padx=0, pady=10)
        lblTime.grid(column=0, row=6, padx=20, pady=20)
        
        cmbTime.grid(column=1, row=6, padx=0, pady=20)
        btnCancel.grid(column=0, row=7)
        btnSubmit.grid(column=1, row=7)

        return addSourceWindow

    def switchStateAdd(*arg):
        global cmbSchedule
        global cmbChangeSchedule
        global cmbTime
        if cmbSelected.get() == "Never":
            cmbChangeSchedule["state"] = "disabled"
            cmbTime["state"] = "disabled"
        else:
            cmbChangeSchedule["state"] = "normal"
            cmbTime["state"] = "normal"

        print("switchStateAdd was run")

    def addSource(self, name, source, destination, schedule, window):
        global location_count
        print(location_count)
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
            self.populate_tree()
       
    ####### Edit Source Window #######
    def openEditSourceWindow(self):
        editSourceWindow = Toplevel(self)
        editSourceWindow.title("Edit Source...")
        editSourceWindow.geometry("400x400")
        editSourceWindow.resizable(False, False)
        global btnEditScheduleEdit
        global cmbSelectedEdit
        global cmbSchedule
        global cmbChangeSchedule
        global cmbTime
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
        cmbSchedule['values'] = ("Never", "Weekly", "Every Two Weeks")
        cmbSchedule.current(current)
        lblWeeks = Label(editSourceWindow, text="Day:")
        lblTime = Label(editSourceWindow, text="Time:")
        cmbChangeSchedule = Combobox(editSourceWindow)
        cmbChangeSchedule['values'] = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
        cmbChangeSchedule.current(0)
        
        spinvar = StringVar()
        
        cmbTime = Combobox(editSourceWindow)
        cmbTime['values'] = ('00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00')
        cmbTime.current(0)
        
        btnCancel = Button(editSourceWindow, text="Cancel", command=editSourceWindow.destroy)
        btnSubmit = Button(editSourceWindow, text="Save", command=lambda: self.editSource(id, txtName.get(), txtSource.get(), txtDestination.get(), cmbSchedule.get(), editSourceWindow))

        #btnEditScheduleEdit = Button(editSourceWindow, text="Change Schedule", state=DISABLED)
        self.readStateEdit()
        lblName.grid(column=0, row=0, padx=50, pady=10)
        txtName.grid(column=1, row=0, padx=10, pady=10)
        lblSource.grid(column=0, row=1, padx=50, pady=10)
        txtSource.grid(column=1, row=1, padx=10, pady=10)
        lblDestination.grid(column=0, row=2, padx=50, pady=10)
        txtDestination.grid(column=1, row=2, padx=10, pady=10)
        lblSchedule.grid(column=0, row=3, padx=50, pady=10)
        cmbSchedule.grid(column=1, row=3, padx=10, pady=10)
        cmbSchedule.bind('<<ComboboxSelected>>', self.switchStateEdit)
        #btnEditScheduleEdit.grid(column=1, row=4, padx=50, pady=10)

        lblWeeks.grid(column=0, row=5, padx=20, pady=10)
        cmbChangeSchedule.grid(column=1, row=5, padx=0, pady=10)
        lblTime.grid(column=0, row=6, padx=20, pady=20)
        
        print(spinvar.get())
        cmbTime.grid(column=1, row=6, padx=0, pady=20)
        
        btnCancel.grid(column=0, row=7, padx=30, pady=10)
        btnSubmit.grid(column=1, row=7, padx=30, pady=10)
        
    def readStateEdit(event):
        global cmbSchedule
        global cmbChangeSchedule
        global cmbTime
        print("event")
        print(event)
        if cmbSchedule.get() == "Never":
           cmbChangeSchedule["state"] = "disabled"
           cmbTime["state"] = "disabled"
        else:
            cmbChangeSchedule["state"] = "normal"
            cmbTime["state"] = "normal"
            
    def switchStateEdit(self, event):
        global cmbSchedule
        global cmbChangeSchedule
        global cmbTime
        if cmbSchedule.get() == "Never":
            cmbChangeSchedule["state"] = "disabled"
            cmbTime["state"] = "disabled"
        else:
            cmbChangeSchedule["state"] = "normal"
            cmbTime["state"] = "normal"
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
            self.populate_tree()
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

            self.populate_tree(self)
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