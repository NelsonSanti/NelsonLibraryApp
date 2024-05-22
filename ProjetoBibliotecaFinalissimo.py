from tkinter import *
from tkinter import ttk
import mysql.connector
import addBook, addMember, deliverBook, removeMember, removeBook
from tkinter import messagebox
connexion=mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@', database='nelsonLibrary')
cursor=connexion.cursor()




class Main(object):
    def __init__(self, master):
        self.master = master

        #to display records
        def displayRecords(event):
            global connexion, cursor
            connexion.close()
            connexion = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@',
                                                database='nelsonLibrary')
            cursor = connexion.cursor()
            cursor.execute("SELECT count(book_id) FROM books")
            count_books = cursor.fetchall()
            cursor.execute("SELECT count(member_id) FROM members")
            count_members = cursor.fetchall()
            cursor.execute("SELECT count(book_status) FROM books WHERE book_status =1")
            taken_books = cursor.fetchall()
            #print(count_books)
            #print(count_members)
            #print(taken_books)
            #labels for display records
            self.lbl_book_count.config(text='Total: ' + str(count_books[0][0]) + ' books in stock')
            self.lbl_member_count.config(text='Total members: ' + str(count_members[0][0]))
            self.lbl_book_taken_count.config(text='Borrowed books: ' + str(taken_books[0][0]))
            displayBooks(self) #3 way. looks easier but with many functions can be complicated.

        # To display books
        def displayBooks(self):
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()
            count = 0
            #delete old values from the list for each update and avoid repetition
            self.list_books.delete(0, END)
            for book in books:
                #print(book)
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

            #list_of_book_details:
            def bookInfo(event):
                #value= str(self.list_books.get(self.list_books.curselection()))
                selected_indices = self.list_books.curselection()
                if selected_indices:
                    index = selected_indices[0]
                    value = str(self.list_books.get(index))
                    id = value.split('-')[0] #to get access to the ids
                    cursor.execute("SELECT * FROM books WHERE book_id =%s", (id,))
                    book_info = cursor.fetchall()
                    #print(book_info)
                    #updating list details
                    self.list_details.delete(0, END) #To avoid pile listing when clicking on the book
                    self.list_details.insert(0, "Book name: " + str(book_info[0][1]))
                    self.list_details.insert(1, "Author: " + str(book_info[0][2]))
                    self.list_details.insert(2, "Page: " + str(book_info[0][3]))
                    self.list_details.insert(3, "Language: " + str(book_info[0][4]))
                    #book borrowed or not
                    if book_info[0][5] == 0:
                        self.list_details.insert(4, "Status: Available!")
                    else:
                        self.list_details.insert(4, "Status: Not available!")

            #function with bind method to lend the books related to members
            def doubleClick(event):
                global delivered_id
                value = str(self.list_books.get(self.list_books.curselection()))
                #print(value) #with bouble click it prints the name of the book
                delivered_id = value.split('-')[0]
                delivered_book= DeliveredBook() #we create another class for get a new window



            self.list_books.bind('<<ListboxSelect>>', bookInfo) #to update the books info while selecting
            self.tabs.bind('<<NotebookTabChanged>>', displayRecords) # 1 way to show updated statistics information
            #self.tabs.bind('<ButtonRelease-1>', displayBooks) # 2 way different to show updated books' list.
            # we will not use it. Because the recommended way is only creating one function instead of
            # the 2 above (display books and display records). Example, create one function named display
            # and the same function contain information for displaybooks and displayrecords and after creating
            # a funcion like NotebooktabChanged which will apply for both
            #see 3 way calling displayBooks function above.
            self.list_books.bind('<Double-Button-1>', doubleClick)




        #frames
        mainFrame = Frame(self.master)
        mainFrame.pack()

        #top frame (child of main frame)
        topFrame = Frame(mainFrame,width=1350,height=70,bg="#f8f8f8",padx=20,relief=SUNKEN,borderwidth=2)
        topFrame.pack(side=TOP,fill=X)

        #center frame (child of main frame)
        centerFrame = Frame(mainFrame,width=1350,relief=RIDGE,bg='#e0f0f0',height=680)
        centerFrame.pack(side=TOP)

        #center left frame (child of center frame)
        centerLeftFrame = Frame(centerFrame,width=900,height=700,bg='#f0f0f0',borderwidth=2,relief='sunken')
        centerLeftFrame.pack(side=LEFT)

        #center right frame (child of center frame)
        centerRightFrame = Frame(centerFrame,width=450,height=700,bg="#f0f0f0",borderwidth=2,relief='sunken')
        centerRightFrame.pack()

        #search bar (child of center right frame)
        search_bar = LabelFrame(centerRightFrame,width=440,height=75,text='Search field',bg='#e6ccb2')
        search_bar.pack(fill=BOTH)

        #Label for search bar
        self.label_search=Label(search_bar,text='Search:',font='BerlinSansFB 12 bold',bg='#e6ccb2',fg='black')
        self.label_search.grid(row=0,column=0,padx=20,pady=10)
        self.entry_search =Entry(search_bar,width=30,bd=5)
        self.entry_search.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        self.button_search= Button(search_bar,text='Search',font='BerlinSansFB 12 bold',bg="#e6ccb2",fg='black',command=self.searchBooks)
        self.button_search.grid(row=0,column=4,padx=20,pady=10)

        #list bar (child of center right frame)
        list_bar = LabelFrame(centerRightFrame,width=440,height=175,text='List field',bg='#b08968')
        list_bar.pack(fill=BOTH)

        #Label for list bar
        self.label_list = Label(list_bar,text='Sort by:',font='BerlinSansFB 12 bold',fg='white',bg='#b08968')
        self.label_list.grid(row=0,column=2)
        self.listChoice = IntVar()
        radiobutton1 = Radiobutton(list_bar, text='All books',var=self.listChoice,value=1, bg='#b08968')
        radiobutton2 = Radiobutton(list_bar, text='In stock',var=self.listChoice,value=2, bg='#b08968')
        radiobutton3 = Radiobutton(list_bar, text='Borrowed books',var=self.listChoice,value=3, bg='#b08968')
        radiobutton1.grid(row=1,column=0)
        radiobutton2.grid(row=1, column=1)
        radiobutton3.grid(row=1, column=2)
        button_list = Button(list_bar,text='Books\' List',bg='#b08968',fg='white',font='BerlinSansFB 12 bold',command=self.listBooks)
        button_list.grid(row=1,column=3,padx=40,pady=10)

        #title and image
        image_bar = Frame(centerRightFrame,width=440,height=350)
        image_bar.pack(fill=BOTH)
        self.title_right = Label(image_bar,text='Welcome to our Library', font='Algerian 16 bold')
        self.title_right.grid(row=0, padx=65)
        self.library_image = PhotoImage(file='library_welcome.png')
        self.lblImg=Label(image_bar,image=self.library_image)
        self.lblImg.grid(row=1, padx=65)

####################################Tools Bar Buttons ###########################################################################


        """#add book button
        self.iconbook =PhotoImage(file='add_book_button.png')
        self.buttonbook = Button(topFrame, text='Add Book', image=self.iconbook,compound=LEFT,padx=10, font='arial 12 bold',command=self.addBook)
        self.buttonbook.pack(side=LEFT)
        #add member button
        self.iconmember = PhotoImage(file='add_member_button.png')
        self.buttonmember = Button(topFrame,text='Add Member',font='arial 12 bold',padx=10,command=self.addMember)
        self.buttonmember.configure(image=self.iconmember,compound=LEFT)
        self.buttonmember.pack(side=LEFT)

        #deliver book button
        self.icondeliver = PhotoImage(file='deliver_book_button.png')
        self.buttondeliver = Button(topFrame, text='Deliver Book',font='arial 12 bold',padx=10, image=self.icondeliver,compound=LEFT,command=self.deliverBookButton)
        self.buttondeliver.pack(side=LEFT)

        #remove member button
        self.iconmember = PhotoImage(file='add_member_button.png')
        self.buttonmember = Button(topFrame, text='Remove Member', font='arial 12 bold', padx=10,
                                   command=self.removeMember)
        self.buttonmember.configure(image=self.iconmember, compound=LEFT)
        self.buttonmember.pack(side=LEFT)

        #remove book button
        self.iconmember = PhotoImage(file='remove_book_button.png')
        self.buttonmember = Button(topFrame, text='Remove Book', font='arial 12 bold', padx=10,
                                   command=self.removeBook)
        self.buttonmember.configure(image=self.iconmember, compound=LEFT)
        self.buttonmember.pack(side=RIGHT)"""

        # Add book button
        self.iconbook = PhotoImage(file='add_book_button.png')
        self.buttonbook = Button(topFrame, text='Add Book', image=self.iconbook, compound=LEFT, padx=10,
                                 font='arial 12 bold', command=self.addBook)
        self.buttonbook.pack(side=LEFT)

        # Add member button
        self.iconmember_add = PhotoImage(file='add_member_button.png')
        self.buttonmember_add = Button(topFrame, text='Add Member', font='arial 12 bold', padx=10,
                                       command=self.addMember)
        self.buttonmember_add.configure(image=self.iconmember_add, compound=LEFT)
        self.buttonmember_add.pack(side=LEFT)

        # Deliver book button
        self.icondeliver = PhotoImage(file='deliver_book_button.png')
        self.buttondeliver = Button(topFrame, text='Deliver Book', font='arial 12 bold', padx=10,
                                    image=self.icondeliver, compound=LEFT, command=self.deliverBookButton)
        self.buttondeliver.pack(side=LEFT)

        # Remove member button
        self.iconmember_remove = PhotoImage(file='add_book_button.png')
        self.buttonmember_remove = Button(topFrame, text='Remove Member', font='arial 12 bold', padx=10,
                                          command=self.removeMember)
        self.buttonmember_remove.configure(image=self.iconmember_remove, compound=LEFT)
        self.buttonmember_remove.pack(side=LEFT)

        # Remove book button
        self.iconbook_remove = PhotoImage(file='remove_book_button.png')
        self.buttonbook_remove = Button(topFrame, text='Remove Book', font='arial 12 bold', padx=10,
                                        command=self.removeBook)
        self.buttonbook_remove.configure(image=self.iconbook_remove, compound=LEFT)
        self.buttonbook_remove.pack(side=LEFT)

        #####################################Tabs #########################################################################################
#####################################Tab1: Management ##############################################################
        self.tabs = ttk.Notebook(centerLeftFrame,width=900,height=660)
        self.tabs.pack()
        self.tab1_icon=PhotoImage(file='management_topline2.png')
        self.tab2_icon=PhotoImage(file='records_topline2.png')
        self.tab1=ttk.Frame(self.tabs)
        self.tab2=ttk.Frame(self.tabs)
        self.tabs.add(self.tab1,text='Management',image=self.tab1_icon,compound=LEFT)
        self.tabs.add(self.tab2,text='Records',image=self.tab2_icon,compound=LEFT)

        #Books' list
        self.list_books = Listbox(self.tab1,width=40,height=26,bd=5,font='times 12 bold')
        self.list_books.grid(row=0, column=0, padx=(10,0), pady=10, sticky=N)
        #scroll bar
        self.sb = Scrollbar(self.tab1,orient=VERTICAL)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)

        #list details
        self.list_details=Listbox(self.tab1,width=80,height=26,bd=5,font='times 12 bold')
        self.list_details.grid(row=0,column=1,padx=(10,0),pady=10,sticky=N)

#######################################Tab2: Records ##########################################################
        self.lbl_book_count = Label(self.tab2,text='',pady=20,font='Univers 14 bold') #text is empty so nothing appears
        # in Records, while anything is written
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count = Label(self.tab2,text='',pady=20,font='Univers 14 bold')
        self.lbl_member_count.grid(row=1,sticky=W)
        self.lbl_book_taken_count = Label(self.tab2,text='',pady=20,font='Univers 14 bold')
        self.lbl_book_taken_count.grid(row=2,sticky=W)

        #calling funcion displayBooks to test in the console
        displayBooks(self)
        #calling function displayRecords to test in the console
        displayRecords(self)

    def addBook(self):
        add=addBook.AddBook() #AddBook is my class created on addBook.py

    def addMember(self):
        member=addMember.AddMember()

    def removeMember(self):
        rmmember = removeMember.RemoveMember()

    def removeBook(self):
        rebook = removeBook.RemoveBook()

    def searchBooks(self):
        value = self.entry_search.get()
        cursor.execute("SELECT * FROM books WHERE book_name LIKE %s",('%' + value + '%',))
        search = cursor.fetchall()
        print(search)
        self.list_books.delete(0, 'end') #To delete the list box after each search
        count=0
        for book in search:
            self.list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1

    def listBooks(self): #function for the 3 little dots (all books, in stock, borrowed)
        value = self.listChoice.get()
        if value == 1:
            cursor.execute("SELECT * FROM books")
            all_books = cursor.fetchall()
            self.list_books.delete(0, 'end')
            count=0
            for book in all_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        elif value == 2:
            cursor.execute("SELECT * FROM books WHERE book_status =%s", (0,))
            books_in_stock = cursor.fetchall()
            self.list_books.delete(0, 'end')
            count = 0
            for book in books_in_stock:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            cursor.execute("SELECT * FROM books WHERE book_status =%s", (1,))
            borrowed_books = cursor.fetchall()
            self.list_books.delete(0, 'end')
            count = 0
            for book in borrowed_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

    def deliverBookButton(self):
        dbbutton = deliverBook.DeliveredBook()

#This is the Deliver book window
class DeliveredBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.iconbitmap("book_ponta.ico")
        self.title("Deliver Book")
        self.resizable(False, False)
        global delivered_id
        self.book_id = int(delivered_id) #int because our delivered_id type is str above and we used split
        # method to create a list.

        #For display list of books in combobox
        cursor.execute("SELECT * FROM books")
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
        self.top_image = PhotoImage(file='add_member_button.png')
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=40)
        #heading = Label(self.topFrame, text=' Add Member ', font='Arial 22 bold', fg='#603808', bg='white')
        #heading.place(x=290, y=60)

        # Entries and Labels
        # Book name
        self.book_name = StringVar()
        self.lbl_book_name = Label(self.buttonFrame, text='Books\' name: ', font='arial 15 bold', fg='white', bg='#8b5e34')
        self.lbl_book_name.place(x=40, y=40)
        self.combo_book_name = ttk.Combobox(self.buttonFrame, textvariable=self.book_name)
        self.combo_book_name['values'] = book_list #displaying the books list
        self.combo_book_name.current(self.book_id-1) #to start the combobox list from the book i clicked
        # (-1 because the indexes start from 0)
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




def main():
    root = Tk()
    app = Main(root)
    root.title("Nelson's Library App")
    root.geometry("1350x750+350+200")
    root.iconbitmap("book_ponta.ico")
    root.mainloop()

"""if __name__ == '__main__':
    main()"""

main()