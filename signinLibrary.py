# -*- coding: utf-8 -*-

#pip install pyinstaller (Criar pastas de distribuição)
# pyinstaller --onefile MusicaApp.py (Criar Pastas)
# pyinstaller MusicaApp.py --onefile --windowed (Atualizar ficheiros sem perder dados)
# pyinstaller --onefile --noconsole MusicaApp.py (Para não abrir a consola no ficheiro executável)

from tkinter import *
from tkinter import messagebox
import time
import mysql.connector
import addBook
import addMember
import deliverBook
import removeBook
import removeMember


##### FRONTEND -------------------------------------
root=Tk()
root.title("Nelson's Library App")
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False,False)
root.iconbitmap("book_ponta.ico")


def guest():
    screen = Toplevel(root)
    screen.iconbitmap("book_ponta.ico")
    screen.title("Nelson's Library App")
    screen.geometry('925x500+300+200')
    screen.config(bg='white')
    Label(screen, text='Welcome to our Library!', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
    screen.update()
    try:
        connexion = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@',
                                                database='nelsonLibrary')
        cursor = connexion.cursor()
        print("Connected to Database!")
        time.sleep(3)
        root.destroy()
        import ProjetoBibFinalGuest
    except:
        messagebox.showerror("Connection Error!", "Database connection not establish!")
        return

    screen.mainloop()

global trial_no
trial_no=0
def trial():
    global trial_no

    trial_no +=1
    print("Number of attempts is: ", trial_no)
    if trial_no == 3:
        messagebox.showwarning("Warning", "You have passed the number of attempts!")
        root.destroy() #program closure

def singin():
    username=user.get()
    pas=password.get()


    if username=='root' and pas=='yQh1iAe17@':
        screen=Toplevel(root)
        screen.iconbitmap("book_ponta.ico")
        screen.title("Nelson's Library App")
        screen.geometry('925x500+300+200')
        screen.config(bg='white')
        Label(screen, text='Welcome to our Library!', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
        screen.update()
        try:
            connexion = mysql.connector.connect(host='localhost', user='root', password='yQh1iAe17@',
                                                database='nelsonLibrary')
            cursor = connexion.cursor()
            print("Connected to Database!")
            time.sleep(3)
            root.destroy()
            import ProjetoBibliotecaFinalissimo
        except Exception as e:
            print(e)
            messagebox.showerror("Connection Error!", "Database connection not establish!")
            return

        screen.mainloop()

    elif username !='root' and pas !='yQh1iAe17@':
        messagebox.showerror("Error!", "Username and Password incorrect")
        trial()
    elif pas !='yQh1iAe17@':
        messagebox.showerror("Error!", "Password is incorrect")
        trial()
    elif username !='root':
        messagebox.showerror("Error!", "Username is incorrect")
        trial()

#### Frame for the Sign in part
img = PhotoImage(file='signinImageLibrary.png')
Label(root,image=img,bg='white').place(x=0,y=0)

frame=Frame(root,width=350,height=370,bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Sign in',fg='#99582a',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)
##### USERNAME-------------------------------------------------------

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name == '':
        user.insert(0, 'Username')

user=Entry(frame,width=30,fg='black',border=2,bg="white",font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)


#Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

##### PASSWORD------------------------------------------------------

def on_enter(e):
    password.delete(0, 'end')

def on_leave(e):
    name=password.get()
    if name == '':
        password.insert(0, 'Password')

password=Entry(frame,width=30,fg='black',border=2,bg="white",font=('Microsoft YaHei UI Light',11))
password.place(x=30,y=150)
password.insert(0, 'Password')
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)

#Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#### SHOW & HIDE EYE------------------------------------------------
button_mode=True

def hide():
    global button_mode

    if button_mode:
        eyeButton.config(image=closed_eye, activebackground="white")
        password.config(show="*")
        button_mode=False
    else:
        eyeButton.config(image=closed_eye, activebackground="white")
        password.config(show="")
        button_mode=True

closed_eye=PhotoImage(file='closed_eye_library.png')
eyeButton=Button(frame,image=closed_eye,bg='white',bd=0,fg='white',font=('Microsoft YaHei UI Light',8),border=0,command=hide)
eyeButton.place(x=280,y=147)

#### BUTTONS -------------------------------------------------------

Button(frame,width=34,pady=7,text='Sign in',bg='#e6ccb2',fg='white',border=2,command=singin).place(x=30,y=204)
label=Label(frame,text="Don't you have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=250)

sign_up= Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#99582a')
sign_up.place(x=135,y=270)

Button(frame,width=34,pady=7,text='Enter as guest',bg='#e6ccb2',fg='white',border=2,command=guest).place(x=30,y=299)


root.mainloop()