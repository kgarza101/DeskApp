from tkinter import *
import sqlite3 

root = Tk()
root.title('To-Do List')

# Create the connector
dataConnector = sqlite3.connect('EntryInfo.db')

# Create Cursor
cursor = dataConnector.cursor()


# Functions
def submit():
    dataConnector = sqlite3.connect('EntryInfo.db')
    cursor = dataConnector.cursor()

    # Varibles in sqlite file
    cursor.execute("INSERT INTO info VALUES(:name, :due_date, :descrip, :status, :group_mem)",
        {
            'name': name.get(),
            'due_date': due_date.get(),
            'descrip': descrip.get(),
            'status': status.get(), 
            'group_mem': group.get()
        }
    )
    dataConnector.commit()
    dataConnector.close()

    name.delete(0, END)
    due_date.delete(0, END)
    descrip.delete(0, END)
    status.delete(0, END)
    group.delete(0, END)
    
    # Refreshes the list
    query_info()


def query_info():
    dataConnector = sqlite3.connect('EntryInfo.db')
    cursor = dataConnector.cursor()

    cursor.execute("SELECT *, oid FROM info")
    records = cursor.fetchall()

    listbox.delete(0, END)

    # Displays the records in order, record 5 is the ID number
    for record in records: 
        listbox.insert(END, f"ID {record[5]} | {record[0]} - {record[1]} - {record[2]} - {record[3]} - {record[4]}")

dataConnector.close()


# User can select the record from the table
def select_record(event):
    try:
        selected = listbox.get(listbox.curselection())
        record_id = selected.split(" ")[1]

        dataConnector = sqlite3.connect('EntryInfo.db')
        cursor = dataConnector.cursor()

        cursor.execute("SELECT * FROM info WHERE oid=?", (record_id,))
        record = cursor.fetchone()

        dataConnector.close()

        name.delete(0, END)
        due_date.delete(0, END)
        descrip.delete(0, END)
        status.delete(0, END)
        group.delete(0, END)

        name.insert(0, record[0])
        due_date.insert(0, record[1])
        descrip.insert(0, record[2])
        status.insert(0, record[3])
        group.insert(0, record[4])

        # Enables the buttons and stores ID
        update_button.config(state = NORMAL)
        delete_button.config(state = NORMAL)
        update_button.record_id = record_id  
    except:
        pass


# Allows the user to update previous record    
def update_record():
    dataConnector = sqlite3.connect('EntryInfo.db')
    cursor = dataConnector.cursor()

    cursor.execute("""UPDATE info SET 
        name = :name,
        due_date = :due_date,
        descrip = :descrip,
        status = :status,
        group_mem = :group_mem
        WHERE oid = :oid""",
        {
            'name': name.get(),
            'due_date': due_date.get(),
            'descrip': descrip.get(),
            'status': status.get(), 
            'group_mem': group.get(),
            'oid': update_button.record_id
        }
    )

    dataConnector.commit()
    dataConnector.close()

    query_info()

    name.delete(0, END)
    due_date.delete(0, END)
    descrip.delete(0, END)
    status.delete(0, END)
    group.delete(0, END)

    update_button.config(state = DISABLED)
    delete_button.config(state = DISABLED)


# Allows the user to delete record from the table    
def delete_record():
    dataConnector = sqlite3.connect('EntryInfo.db')
    cursor = dataConnector.cursor()

    cursor.execute("DELETE FROM info WHERE oid=?", (update_button.record_id,))
    dataConnector.commit()
    dataConnector.close()

    # Refresh the list
    query_info()

    # Clear entry fields
    name.delete(0, END)
    due_date.delete(0, END)
    descrip.delete(0, END)
    status.delete(0, END)
    group.delete(0, END)

    update_button.config(state = DISABLED)
    delete_button.config(state = DISABLED)


# GUI section
# Widgets
name = Entry(root, width = 50)
due_date = Entry(root, width = 50)
descrip = Entry(root, width = 50)
status = Entry(root, width = 50)
group = Entry(root, width = 50)

name_label = Label(root, text = "Name")
date_label = Label(root, text = "Due Date")
descrip_label = Label(root, text = "Description")
status_label = Label(root, text = "Status")
group_label = Label(root, text = "Group Members")

submit_button = Button(root, text="Add Data", command = submit)
update_button = Button(root, text="Update Data", command = update_record, state = DISABLED)
delete_button = Button(root, text="Delete Data", command = delete_record, state = DISABLED)

# Table to display records
listbox = Listbox(root, width = 75, height = 10)
listbox.bind("<<ListboxSelect>>", select_record)
scrollbar = Scrollbar(root, orient = VERTICAL, command = listbox.yview)
listbox.config(yscrollcommand = scrollbar.set)

# Layout
name.grid(row = 0, column = 1)
due_date.grid(row = 1, column = 1)
descrip.grid(row = 2, column = 1)
status.grid(row = 3, column = 1)
group.grid(row = 4, column = 1)

name_label.grid(row = 0, column = 0)
date_label.grid(row = 1, column = 0)
descrip_label.grid(row = 2, column = 0)
status_label.grid(row = 3, column = 0)
group_label.grid(row = 4, column = 0)

submit_button.grid(row = 5, column = 0)
update_button.grid(row = 7, column = 0)
delete_button.grid(row = 8, column = 0)

listbox.grid(row = 6, column = 0, columnspan = 2)
scrollbar.grid(row = 6, column = 2, sticky = 'ns')

query_info()

root.mainloop()
