import pymysql
from tkinter import *
from tkinter import messagebox
from pymysql.err import Error

try:
    fp = open("database_details.txt","r")
    mysql_user, mysql_pass = fp.read().split(" ")
    print(mysql_user, "->", mysql_pass)
    conn = pymysql.connect(host="localhost", user=mysql_user, password=mysql_pass, db="webscraper")
    curs = conn.cursor()
except:
    mysql_user = input("enter root username for mysql: ")
    mysql_pass = input("enter root password for mysql: ")
    fp = open("database_details.txt", "w")
    fp.writelines([mysql_user, " ", mysql_pass])
    conn = pymysql.connect(host="localhost", user=mysql_user, password=mysql_pass, db="webscraper")
    curs = conn.cursor()
    try:
        sqlQuery = "USE webscraper;"
        curs.execute()
        sqlQuery = "CREATE TABLE login_details(username varchar(30) primary key, password varchar(50));"
        curs.execute()
        conn.commit()
    except:
        print("Unable to create database")
        pass

class LoginPage():
    def __init__(self, master, socialmedia):
        self.master = master
        self.socialmedia = socialmedia
        master.label_username = Label(master, text="Username")
        master.label_username.config(width=10)
        master.entry_username = Entry(master)
        master.label_username.grid(row=0, column=0,sticky=E)
        master.entry_username.grid(row=0, column=1)

        master.label_password = Label(master, text="Password")
        master.entry_password = Entry(master, show="•")
        master.label_password.grid(row=1, column=0, sticky=E)
        master.entry_password.grid(row=1, column=1)

        login_button = Button(master, text="Login", command=lambda: self.validate(master.entry_username.get(), master.entry_password.get()))
        login_button.grid(columnspan=2)

        register_button = Button(master, text="Register", command=self.register)
        register_button.grid(columnspan=2)

    def validate(self, username, passwordB):
        sqlQuery = "SELECT password FROM login_details WHERE username="+repr(username)
        curs.execute(sqlQuery)
        passwordA = curs.fetchone()
        if not passwordA:
            messagebox.showerror(title='Error', message='Invalid Username')
        elif passwordA[0] != passwordB:
            messagebox.showerror(title='Error', message='Invalid Password')
        else:
            messagebox.showinfo(title='Success', message='Login Successful')
            conn.close()
            self.master.destroy()
            self.socialmedia.enter()

    def reg(self):
        username = self.master.entry_username.get()
        password = self.master.entry_password.get()
        try:
            sqlQuery = "INSERT INTO login_details VALUES("+repr(username)+", "+repr(password)+")"
            curs.execute(sqlQuery)
            conn.commit()
            messagebox.showinfo(title='Success', message='Registration Successful')
            conn.close()
            self.master.destroy()
            self.socialmedia.enter()
        except Error as e:
            messagebox.showerror(title='Error', message='Such User already exists')

    def register(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.master.label_username = Label(self.master, text="Username")
        self.master.label_username.config(width=10)
        self.master.entry_username = Entry(self.master)
        self.master.label_username.grid(row=0, column=0, sticky=E)
        self.master.entry_username.grid(row=0, column=1)

        self.master.label_password = Label(self.master, text="Password")
        self.master.entry_password = Entry(self.master)
        self.master.label_password.grid(row=2, column=0, sticky=E)
        self.master.entry_password.grid(row=2, column=1)

        register_button = Button(self.master, text="Register", command=self.reg)
        register_button.grid(columnspan=2)