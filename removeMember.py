from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

connexion = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@', database='nelsonLibrary')
cursor = connexion.cursor()


class RemoveMember(Toplevel):
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
        self.title("Remove Member")
        self.resizable(False, False)
        self.iconbitmap("book_ponta.ico")

        # For display list of members in combobox
        cursor.execute("SELECT * FROM members")
        query2 = cursor.fetchall()
        member_list = []
        for member in query2:
            member_list.append(str(member[0]) + "-" + member[1])

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
        heading = Label(self.topFrame, text=' Remove Member ', font='Arial 22 bold', fg='#603808', bg='white')
        heading.place(x=290, y=60)

        # Entries and Labels
        # member name
        self.member_name = StringVar()
        self.lbl_member_name = Label(self.buttonFrame, text='Member\'s name: ', font='arial 15 bold', fg='white',
                                     bg='#8b5e34')
        self.lbl_member_name.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.buttonFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list  # We dont know which member so we just display the list
        self.combo_member.place(x=200, y=85)

        # button
        button = Button(self.buttonFrame, text='Remove member', command=self.removeMember)
        button.place(x=270, y=120)

    def removeMember(self):
        member_name = self.member_name.get()
        if member_name:
            try:
                member_id = member_name.split('-')[0]
                cursor.execute("DELETE FROM members WHERE member_id =%s",
                               (member_id,))
                connexion.commit()
                messagebox.showinfo("Success!", "The member was removed from the database", icon='info')

            except Error as e:
                messagebox.showerror("Error!", f"The member was not removed from the database: {e}", icon='warning')
        else:
            messagebox.showerror("Error!", "Please, fill in all fields", icon='warning')






