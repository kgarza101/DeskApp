import sqlite3 
from tkinter import *
from tkinter import messagebox
import login_system

class TaskManagerApp:
    def __init__(self, root, is_admin = False):
        self.root = root 
        self.is_admin = is_admin
        self.root.geometry("650x500")
        self.root.title('To-Do List - Admin Mode' if is_admin else 'To-Do List - User Mode')
        
        self.dataConnector = sqlite3.connect('EntryInfo.db')
        self.cursor = self.dataConnector.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS info 
                            (name TEXT, due_date TEXT, descrip TEXT, status TEXT, group_mem TEXT)''')
        self.dataConnector.commit()
        self.create_widgets()
        self.query_info()
        
        if not self.is_admin:
            self.disable_admin_features()
            
    def create_widgets(self):
        self.name = Entry(self.root, width = 50)
        self.due_date = Entry(self.root, width = 50)
        self.descrip = Entry(self.root, width = 50)
        self.status = Entry(self.root, width = 50)
        self.group = Entry(self.root, width = 50)
        
        self.title_label = Label(root, text="Welcome to Your Task Assigner", fg="dark green", font=("Times New Roman", 25, "bold"))
        self.name_label = Label(self.root, text = "Name")
        self.date_label = Label(self.root, text = "Due Date")
        self.descrip_label = Label(self.root, text = "Description")
        self.status_label = Label(self.root, text = "Status")
        self.group_label = Label(self.root, text = "Group Members")
        
        self.submit_button = Button(self.root, text = "Add Data", command = self.submit)
        self.update_button = Button(self.root, text = "Update Data", command = self.update_record, state = DISABLED)
        self.delete_button = Button(self.root, text = "Delete Data", foreground="snow", command = self.delete_record, state=DISABLED)
        self.select_button = Button(self.root, text = "Select Task", command = self.select_task)
        
        # Table to display records
        self.listbox = Listbox(self.root, width = 75, height = 10)
        self.listbox.bind("<<ListboxSelect>>", self.select_record)
        self.scrollbar = Scrollbar(self.root, orient = VERTICAL, command = self.listbox.yview)
        self.listbox.config(yscrollcommand = self.scrollbar.set)   
        
        #Color
        self.root.configure(background="lightblue")
        self.title_label.config(background="lightblue")
        #change button color to tell difference
        #self.delete_button.config(background="red")

        # Layout
        self.name.place(x=175, y=75)
        self.due_date.place(x=175, y=100)
        self.descrip.place(x=175, y=125)
        self.status.place(x=175, y=150)
        self.group.place(x=175, y=175)
        self.title_label.place(x=50, y=0, width=550, relheight=0.1)

        self.name_label.place(x=128, y=75)
        self.date_label.place(x=112, y=100)
        self.descrip_label.place(x=100, y=125)
        self.status_label.place(x=128, y=150)
        self.group_label.place(x=75, y=175)  
        
        if self.is_admin:
            self.submit_button.place(x=450, y=205)
            self.update_button.place(x=150, y=425)
            self.delete_button.place(x=480, y=425)
        
        self.select_button.place(x=560, y=390)
        self.listbox.place(x=150, y=250, width=375)
        self.scrollbar.place(x=535, y=250, height=165)
    
    def disable_admin_features(self):
        self.name.config(state = DISABLED)
        self.due_date.config(state = DISABLED)
        self.descrip.config(state = DISABLED)
        self.status.config(state = DISABLED)
        self.group.config(state = DISABLED)
        self.submit_button.config(state = DISABLED)        
    
    def submit(self):
        self.dataConnector = sqlite3.connect('EntryInfo.db')
        self.cursor = self.dataConnector.cursor()

        self.cursor.execute("INSERT INTO info VALUES(:name, :due_date, :descrip, :status, :group_mem)",
            {
                'name': self.name.get(),
                'due_date': self.due_date.get(),
                'descrip': self.descrip.get(),
                'status': self.status.get(), 
                'group_mem': self.group.get()
            }
        )
        self.dataConnector.commit()
        self.dataConnector.close()

        self.name.delete(0, END)
        self.due_date.delete(0, END)
        self.descrip.delete(0, END)
        self.status.delete(0, END)
        self.group.delete(0, END)
        
        self.query_info()
    
    def query_info(self):
        self.dataConnector = sqlite3.connect('EntryInfo.db')
        self.cursor = self.dataConnector.cursor()

        self.cursor.execute("SELECT *, oid FROM info")
        records = self.cursor.fetchall()

        self.listbox.delete(0, END)

        for record in records: 
            self.listbox.insert(END, f"ID {record[5]} | {record[0]} - {record[1]} - {record[2]} - {record[3]} - {record[4]}")

        self.dataConnector.close()
    
    def select_record(self, event):
        try:
            selected = self.listbox.get(self.listbox.curselection())
            record_id = selected.split(" ")[1]

            self.dataConnector = sqlite3.connect('EntryInfo.db')
            self.cursor = self.dataConnector.cursor()

            self.cursor.execute("SELECT * FROM info WHERE oid=?", (record_id,))
            record = self.cursor.fetchone()

            self.dataConnector.close()

            self.name.delete(0, END)
            self.due_date.delete(0, END)
            self.descrip.delete(0, END)
            self.status.delete(0, END)
            self.group.delete(0, END)

            self.name.insert(0, record[0])
            self.due_date.insert(0, record[1])
            self.descrip.insert(0, record[2])
            self.status.insert(0, record[3])
            self.group.insert(0, record[4])

            if self.is_admin:
                self.update_button.config(state=NORMAL)
                self.delete_button.config(state=NORMAL)
                self.update_button.record_id = record_id
        except:
            pass
        
    def update_record(self):
        self.dataConnector = sqlite3.connect('EntryInfo.db')
        self.cursor = self.dataConnector.cursor()
        
        self.cursor.execute("""UPDATE info SET 
            name = :name,
            due_date = :due_date,
            descrip = :descrip,
            status = :status,
            group_mem = :group_mem
            WHERE oid = :oid""",
            {
                'name': self.name.get(),
                'due_date': self.due_date.get(),
                'descrip': self.descrip.get(),
                'status': self.status.get(), 
                'group_mem': self.group.get(),
                'oid': self.update_button.record_id
            }
        )
        
        self.dataConnector.commit()
        self.dataConnector.close()
        self.query_info()
        
        self.name.delete(0, END)
        self.due_date.delete(0, END)
        self.descrip.delete(0, END)
        self.status.delete(0, END)
        self.group.delete(0, END)
        
        self.update_button.config(state = DISABLED)
        self.delete_button.config(state = DISABLED)
        
    def delete_record(self):
        # Create the connector
        self.dataConnector = sqlite3.connect('EntryInfo.db')
        # Create Cursor
        self.cursor = self.dataConnector.cursor()
       
        self.cursor.execute("DELETE FROM info WHERE oid=?", (self.update_button.record_id,))
        self.dataConnector.commit()
        self.dataConnector.close()

        self.query_info()

        self.name.delete(0, END)
        self.due_date.delete(0, END)
        self.descrip.delete(0, END)
        self.status.delete(0, END)
        self.group.delete(0, END)

        self.update_button.config(state = DISABLED)
        self.delete_button.config(state = DISABLED)    
        
    def select_task(self):
        try:
            selected = self.listbox.get(self.listbox.curselection())
            messagebox.showinfo("Task Selected", f"You've selected: {selected}")
        except:
            messagebox.showerror("Error", "Please select a task first.")
            
if __name__ == "__main__":
    root = Tk()
    app = TaskManagerApp(root, is_admin = True)
    root.mainloop()
