from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import mysql.connector
from mysql.connector import Error

connexion = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@', database='nelsonLibrary')
cursor = connexion.cursor()


class RemoveBook(Toplevel):
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
        self.title("Remove Book")
        self.resizable(False, False)
        self.iconbitmap("book_ponta.ico")

        # For display list of books in combobox
        cursor.execute("SELECT * FROM books")  # To show only the available books.
        # Without "WHERE", all books are showned.
        query = cursor.fetchall()
        book_list = []
        for book in query:
            book_list.append(str(book[0]) + "-" + book[1])

        # Frames
        # Top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Button Frame
        self.buttonFrame = Frame(self, height=600, bg='#8b5e34')
        self.buttonFrame.pack(fill=X)

        # Heading and image
        self.top_image = PhotoImage(file='remove_book_button.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=40)
        heading = Label(self.topFrame, text=' Remove Book ', font='Arial 22 bold', fg='#603808', bg='white')
        heading.place(x=290, y=60)

        # Entries and Labels
        # member name
        self.book_name = StringVar()
        self.lbl_book_name = Label(self.buttonFrame, text='Books\' name: ', font='arial 15 bold', fg='white',
                                   bg='#8b5e34')
        self.lbl_book_name.place(x=40, y=40)
        self.combo_book_name = ttk.Combobox(self.buttonFrame, textvariable=self.book_name)
        self.combo_book_name['values'] = book_list  # displaying the books list
        self.combo_book_name.place(x=200, y=45)

        # button
        button = Button(self.buttonFrame, text='Remove Book', command=self.removeBook)
        button.place(x=270, y=120)

    def removeBook(self):
        book_name = self.book_name.get()
        if book_name:
            try:
                book_id = book_name.split('-')[0]
                cursor.execute("DELETE FROM books WHERE book_id =%s",
                               (book_id,))
                connexion.commit()
                messagebox.showinfo("Success!", "The member was removed from the database", icon='info')

            except Error as e:
                messagebox.showerror("Error!", f"The member was not removed from the database: {e}", icon='warning')
        else:
            messagebox.showerror("Error!", "Please, fill in all fields", icon='warning')






