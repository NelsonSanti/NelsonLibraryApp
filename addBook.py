from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
connexion=mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@', database='nelsonLibrary')
cursor=connexion.cursor()

                

class AddBook(Toplevel):
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
        self.title("Add Book")
        self.resizable(False,False)
        self.iconbitmap("book_ponta.ico")


        #Frames
        #Top Frame
        self.topFrame=Frame(self,height=150,bg='white')
        self.topFrame.pack(fill=X)

        #Button Frame
        self.buttonFrame=Frame(self,height=600,bg='#8b5e34')
        self.buttonFrame.pack(fill=X)

        #Heading and image
        self.top_image = PhotoImage(file='add_book_button.png')
        top_image_lbl=Label(self.topFrame,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=40)
        heading=Label(self.topFrame,text=' Add Book ',font='Arial 22 bold',fg='#603808',bg='white')
        heading.place(x=290,y=60)

        #Entries and Labels
        #name of the book
        self.lbl_name=Label(self.buttonFrame, text='Name: ',font='arial 15 bold',fg='white',bg='#8b5e34')
        self.lbl_name.place(x=40,y=40)
        self.entry_name=Entry(self.buttonFrame,width=30,border=4)
        self.entry_name.insert(0,'Please insert the books\' name')
        self.entry_name.place(x=150,y=45)

        #author of the book
        self.lbl_author = Label(self.buttonFrame, text='Author: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_author.place(x=40, y=80)
        self.entry_author = Entry(self.buttonFrame, width=30, border=4)
        self.entry_author.insert(0, 'Please insert the books\' author')
        self.entry_author.place(x=150, y=85)

        #page
        self.lbl_page = Label(self.buttonFrame, text='Page: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_page.place(x=40, y=120)
        self.entry_page = Entry(self.buttonFrame, width=30, border=4)
        self.entry_page.insert(0, 'Please insert total books\' pages')
        self.entry_page.place(x=150, y=125)

        #language
        self.lbl_language = Label(self.buttonFrame, text='Language: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_language.place(x=40, y=160)
        self.entry_language = Entry(self.buttonFrame, width=30, border=4)
        self.entry_language.insert(0, 'Please insert an idiom')
        self.entry_language.place(x=150, y=165)

        #button
        button=Button(self.buttonFrame,text='Add Book', command=self.addBook)
        button.place(x=270,y=200)




    def addBook(self):
        name = self.entry_name.get()
        author = self.entry_author.get()
        page = self.entry_page.get()
        language = self.entry_language.get()

        if name and author and page and language != "":
            try:
                cursor.execute("INSERT INTO books (book_name,book_author,book_page,book_language) VALUES(%s,%s,%s,%s)",
                               (name, author, page, language))
                connexion.commit()
                messagebox.showinfo("Success!", "The book was added to the database", icon='info')

            except Error as e:
                messagebox.showerror("Error!",f"The book was not added to the database: {e}",icon='warning')
        else:
            messagebox.showerror("Error!", "Please, fill in all fields", icon='warning')






