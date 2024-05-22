from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

connexion = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@', database='nelsonLibrary')
cursor = connexion.cursor()


class AddMember(Toplevel):
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@',
                                                database='nelsonLibrary')
            if self.conn.is_connected():
                print("My SQL Workbench is connected")
                self.cursor = self.conn.cursor()
        except Error as e:
            print(f"Error while connecting to My SQL Workbench: {e}")
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Member")
        self.resizable(False, False)
        self.iconbitmap("book_ponta.ico")

        # Frames
        # Top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Button Frame
        self.buttonFrame = Frame(self, height=600, bg='#8b5e34')
        self.buttonFrame.pack(fill=X)

        # Heading and image
        self.top_image = PhotoImage(file='add_member_button.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=40)
        heading = Label(self.topFrame, text=' Add Member ', font='Arial 22 bold', fg='#603808', bg='white')
        heading.place(x=290, y=60)

        # Entries and Labels
        # name member
        self.lbl_name = Label(self.buttonFrame, text='Name: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_name.place(x=40, y=40)
        self.entry_name = Entry(self.buttonFrame, width=30, border=4)
        self.entry_name.insert(0, 'Please insert the books\' name')
        self.entry_name.place(x=150, y=45)

        # phone
        self.lbl_phone = Label(self.buttonFrame, text='Phone: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_phone.place(x=40, y=80)
        self.entry_phone = Entry(self.buttonFrame, width=30, border=4)
        self.entry_phone.insert(0, 'Please insert the phone number')
        self.entry_phone.place(x=150, y=85)


        # button
        button = Button(self.buttonFrame, text='Add Member', command=self.addMember)
        button.place(x=270, y=120)

    def addMember(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()

        if name and phone != "":
            try:
                cursor.execute("INSERT INTO members (member_name,member_phone) VALUES(%s,%s)",
                               (name, phone))
                connexion.commit()
                messagebox.showinfo("Success!", "The member was added to the database", icon='info')

            except Error as e:
                messagebox.showerror("Error!", f"The member was not added to the database: {e}", icon='warning')
        else:
            messagebox.showerror("Error!", "Please, fill in all fields", icon='warning')






