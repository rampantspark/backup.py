from ast import Return
from imp import source_from_cache
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import json
# Counter for JSON locations
location_count = 0
# Init Root Window
root = Tk()
# Set Root Window Title
root.title("Backup.py")
# Populate the Tree View Widget
def populateTree():
    global location_count
    #Read from json file and populate treelist
    with open("locations.json", "r") as file:
        data = json.loads(file.read())
        testDict = {}
        testDict = data

    for d in data:
        tree.insert('', END, values=(d['id'], d['name'], d['source'], d['destination'], d['schedule']))
        location_count +=1
        print(location_count)
# Clear data from the Tree View Widget
def clearTree():
    #clear the tree
    for item in tree.get_children():
            tree.delete(item)
####### Add Source Window #######
def openAddSourceWindow():
    # Toplevel object which will
    # be treated as a new window
    addSourceWindow = Toplevel(root)

    # sets the title of the
    # Toplevel widget
    addSourceWindow.title("Add Source...")

    # sets the geometry of toplevel
    addSourceWindow.geometry("400x300")

    lblName = Label(addSourceWindow, text="Name:")
    txtName = Entry(addSourceWindow)
    lblSource = Label(addSourceWindow, text="Source:")
    txtSource = Entry(addSourceWindow)
    lblDestination = Label(addSourceWindow, text="Destination:")
    txtDestination = Entry(addSourceWindow)
    lblSchedule = Label(addSourceWindow, text="Schedule:")
    cmbSchedule = Combobox(addSourceWindow)
    cmbSchedule['values'] = ("Never", "Weekly", "Every Two Weeks")
    cmbSchedule.current(0)
    btnCancel = Button(addSourceWindow, text="Cancel", command=addSourceWindow.destroy)
    btnSubmit = Button(addSourceWindow, text="Okay", command=lambda: addSource(txtName.get(), txtSource.get(), txtDestination.get(), cmbSchedule.get(), addSourceWindow))

    lblName.grid(column=0, row=0, padx=50, pady=10)
    txtName.grid(column=1, row=0, padx=10, pady=10)
    lblSource.grid(column=0, row=1, padx=50, pady=10)
    txtSource.grid(column=1, row=1, padx=10, pady=10)
    lblDestination.grid(column=0, row=2, padx=50, pady=10)
    txtDestination.grid(column=1, row=2, padx=10, pady=10)
    lblSchedule.grid(column=0, row=3, padx=50, pady=10)
    cmbSchedule.grid(column=1, row=3, padx=10, pady=10)
    btnCancel.grid(column=0, row=4)
    btnSubmit.grid(column=1, row=4)

    return addSourceWindow
# Add Source Logic
def addSource(name, source, destination, schedule, window):
    global location_count
    print(name + source + destination)
    # Make sure the data to save exists
    if not name or not source or not destination:
        messagebox.showwarning("Add Source", "Please make sure all fields are populated...")
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
                "schedule" : schedule
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
        clearTree()
        # Reset location count
        location_count = 0
        # Populate the Tree View
        populateTree()
####### Edit Source Window #######
def openEditSourceWindow():
    # Toplevel object which will
    # be treated as a new window
    editSourceWindow = Toplevel(root)
    # sets the title of the
    # Toplevel widget
    editSourceWindow.title("Add Source...")
    # sets the geometry of toplevel
    editSourceWindow.geometry("400x300")
    # Get the currently selected tree view item
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
        #throw and exception
        current=3

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
    btnCancel = Button(editSourceWindow, text="Cancel", command=editSourceWindow.destroy)
    btnSubmit = Button(editSourceWindow, text="Add", command=lambda: editSource(id, txtName.get(), txtSource.get(), txtDestination.get(), cmbSchedule.get(), editSourceWindow))

    lblName.grid(column=0, row=0, padx=50, pady=10)
    txtName.grid(column=1, row=0, padx=10, pady=10)
    lblSource.grid(column=0, row=1, padx=50, pady=10)
    txtSource.grid(column=1, row=1, padx=10, pady=10)
    lblDestination.grid(column=0, row=2, padx=50, pady=10)
    txtDestination.grid(column=1, row=2, padx=10, pady=10)
    lblSchedule.grid(column=0, row=3, padx=50, pady=10)
    cmbSchedule.grid(column=1, row=3, padx=10, pady=10)
    btnCancel.grid(column=0, row=4)
    btnSubmit.grid(column=1, row=4)
# Edit Source Logic
def editSource(id, name, source, destination, schedule, window):
    print(name + source + destination)

    if not name or not source or not destination:
        messagebox.showwarning("Edit Source", "Please make sure all fields are populated...")
    else:
        window.destroy()

        data = {
                "id" : id,
                "name" : name,
                "source" : source,
                "destination" : destination,
                "schedule" : schedule
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
        clearTree()
        #populate the treeview
        populateTree()
# Remove Source Logic
def removeSource():
   global location_count
   confirm = messagebox.askokcancel("Remove Source...", "Are you sure you want to remove this backup location?")

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
       clearTree()

       location_count = 0

       populateTree()
   else:
       reply = "cancel"
# Individual Backup Logic
def backup():
    #Do this
    messagebox.showwarning("Remove Source...", "Are you sure you want to remove this backup location?")
# Backup All Logic
def backupAll():
    #Do this
    messagebox.showwarning("Remove Source...", "Are you sure you want to remove this backup location?")
####### The Main Window #######
# Define Tree View Coumns
columns = ('id', 'name', 'source', 'destination', 'last_backup', 'next_backup', 'status')
# Define Title Label
lblTitle = Label(root, text="Backup.py", font=("Arial", 25))
# Define Tree View Frame
frame = Frame(root)
# Define Tree View
tree = Treeview(frame, columns=columns, show="headings")

tree.heading('id', text="ID")
tree.heading('name', text="Name")
tree.heading('source', text="Source")
tree.heading('destination', text="Destination")
tree.heading('last_backup', text="Last Backup")
tree.heading('next_backup', text="Next Backup")
tree.heading('status', text="Status")
# Define Tree View Scrollbar
scrlTree = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrlTree.set)
# Main Functionality Buttons
btnAdd = Button(root, text="Add Source...", command=openAddSourceWindow)
btnEdit = Button(root, text="Edit Source...", command=openEditSourceWindow)
btnDelete = Button(root, text="Remove Source...", command=removeSource)
btnBackup = Button(root, text="Backup Now...")
# Push Title to Grid
lblTitle.grid(column=0, row=0, columnspan=4, padx=0, pady=30)
# Push the Frame, Tree View, and Scrollbar to Grid
frame.grid(column=0, row=1, columnspan=4, padx=20, pady=20)
tree.grid(column=0, row=1, columnspan=4, padx=0, pady=0, sticky='nsew')
scrlTree.grid(column=4, row=1, padx=0, sticky="ns")
# Populate the Tree with JSON location data
populateTree()
# Push Main Functionality Buttons to Grid
btnAdd.grid(column=0, row=4, padx=15, pady=20)
btnEdit.grid(column=1, row=4, padx=15, pady=20)
btnDelete.grid(column=2, row=4, padx=15, pady=20)
btnBackup.grid(column=3, row=4, padx=15, pady=20)
# Run the Main Loop
root.mainloop()
