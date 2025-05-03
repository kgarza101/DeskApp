import sqlite3
from tkinter import *
from tkinter import messagebox
import Desk_App

def setup_user_db():
    conn = sqlite3.connect('user_credentials.db')
    c = conn.cursor()
    
    # Creates the database infile
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, is_admin INTEGER)''')
    
    c.execute("SELECT * FROM users WHERE username ='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users VALUES ('admin', 'admin123', 1)")    
    conn.commit()
    conn.close()
    
class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Task Manager - Login")
        master.geometry("300x150")
        
        setup_user_db()
        
        # Widgets and Layout
        self.text = Label(master, text = "Please log in or sign up", fg="gray12", font=("Times New Roman", 11))
        self.label_username = Label(master, text = "Username: ")
        self.label_password = Label(master, text = "Password: ")
        
        self.entry_username = Entry(master)
        self.entry_password = Entry(master, show = "*")
        
        self.button_login = Button(master, text = "Login", command = self.login)
        self.button_signup = Button(master, text = "Sign up", command = self.open_signup)
        
        self.text.place(x=85, y=15)
        self.label_username.place(x=30, y=45)#(row = 0, column = 0, padx = 5, pady = 5)
        self.label_password.place(x=30, y=75)#(row = 1, column = 0, padx = 5, pady = 5)
        
        self.entry_username.place(x=95, y=45)#(row = 0, column = 1, padx = 5, pady = 5)
        self.entry_password.place(x=95, y=77)#(row = 1, column = 1, padx = 5, pady = 5)
        
        self.button_login.place(x=170, y=110)#(row = 2, column = 0, padx = 5, pady = 5)
        self.button_signup.place(x=95, y=110)#(row = 2, column = 1, padx = 5, pady = 5)
        
        #color
        self.master.configure(background="pale green")
        self.label_username.config(background="pale green")
        self.label_password.config(background="pale green")
        self.text.config(background="pale green")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
    
        # Admin view
        if user:
            self.master.destroy()
            root = Tk()
            is_admin = user[2] == 1
            app = Desk_App.TaskManagerApp(root, is_admin)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
           
    def open_signup(self):
        signup_window = Toplevel(self.master)
        SignupWindow(signup_window)
        
        
class SignupWindow:
    def __init__(self, master):
        self.master = master
        master.title("Sign Up")
        master.geometry("300x190")

        
        # Widgets and Layout
        self.label_username = Label(master, text = "New Username: ")
        self.label_password = Label(master, text = "New Password: ")
        self.label_confirm = Label(master, text = "Confirm Password: ")
        self.text_label = Label(master, text= "Please Sign-Up to Gain Access", font=("Times New Roman", 10))
        
        self.entry_username = Entry(master)
        self.entry_password = Entry(master, show = "*")
        self.entry_confirm = Entry(master, show = "*")
        
        self.button_signup = Button(master, text = "Create Account", command = self.signup)
        
        self.text_label.place(x=60, y=12)
        self.label_username.place(x=35, y=50)
        self.label_password.place(x=35, y=80)
        self.label_confirm.place(x=35, y=110)
        
        self.entry_username.place(x=150, y=50)
        self.entry_password.place(x=150, y=80)
        self.entry_confirm.place(x=150, y=110)
        
        self.button_signup.place(x=115, y=150)  

        #Color
        self.master.configure(background="lightsteelblue1")
        self.text_label.config(background="lightsteelblue1")
        self.label_confirm.config(background="lightsteelblue1")
        self.label_password.config(background="lightsteelblue1")
        self.label_username.config(background="lightsteelblue1")
        
    def signup(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords don't match!")
            return 
        
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required!")
            return
            
        conn = sqlite3.connect('user_credentials.db')
        c = conn.cursor()
        
        try:
            c.execute("INSERT INTO users VALUES (?, ?, 0)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.master.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()
            
if __name__ == "__main__":
    root = Tk()
    login_app = LoginWindow(root)
    root.mainloop()