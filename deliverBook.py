from tkinter import *
from tkinter import ttk
import mysql.connector
import addBook, addMember, deliverBook
from tkinter import messagebox
connexion=mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@', database='nelsonLibrary')
cursor=connexion.cursor()

class DeliveredBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.iconbitmap("book_ponta.ico")
        self.title("Deliver Book")
        self.resizable(False, False)


        #For display list of books in combobox
        cursor.execute("SELECT * FROM books WHERE book_status =0") #To show only the available books.
        # Without "WHERE", all books are showned.
        query = cursor.fetchall()
        book_list = []
        for book in query:
            book_list.append(str(book[0])+"-"+book[1])
        # For display list of members in combobox
        cursor.execute("SELECT * FROM members")
        query2 = cursor.fetchall()
        member_list = []
        for member in query2:
            member_list.append(str(member[0])+"-"+member[1])

        # Frames
        # Top Frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Button Frame
        self.buttonFrame = Frame(self, height=600, bg='#8b5e34')
        self.buttonFrame.pack(fill=X)

        # Heading and image
        self.top_image = PhotoImage(file='deliver_book_button.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=40)
        heading = Label(self.topFrame, text=' Deliver a book ', font='Arial 22 bold', fg='#603808', bg='white')
        heading.place(x=290, y=60)

        # Entries and Labels
        # Book name
        self.book_name = StringVar()
        self.lbl_book_name = Label(self.buttonFrame, text='Books\' name: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_book_name.place(x=40, y=40)
        self.combo_book_name = ttk.Combobox(self.buttonFrame, textvariable=self.book_name)
        self.combo_book_name['values'] = book_list #displaying the books list
        self.combo_book_name.place(x=200,y=45)


        # member name
        self.member_name = StringVar()
        self.lbl_member_name = Label(self.buttonFrame, text='Member\'s name: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_member_name.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.buttonFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list #We dont know which member so we just display the list
        self.combo_member.place(x=200, y=85)

        # button
        button = Button(self.buttonFrame, text='Deliver book', command=self.deliverBook)
        button.place(x=267, y=120)

    def deliverBook(self):
        book_name = self.book_name.get()
        self.book_id = book_name.split('-')[0]
        member_name = self.member_name.get()

        if book_name and member_name != "":
            try:
                cursor.execute("INSERT INTO borrows (bbook_id,bmember_id) VALUES(%s,%s)",
                               (book_name,member_name))
                connexion.commit()
                messagebox.showinfo("Success!", "Borrowed book added to database!", icon='info')
                #We need to update automatically our borrows table once a book is landed so:
                cursor.execute("UPDATE books SET book_status =%s WHERE book_id =%s",(1,self.book_id))
                connexion.commit()
            except Exception as e:
                print(e)
                messagebox.showerror("Error!", "Borrowed book was not added to the database!",icon='warning')
        else:
            messagebox.showerror("Error!", "Please, fulfill all the fields",icon='warning')