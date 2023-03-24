from tkinter import*
from tkinter.colorchooser import askcolor


myWindow=Tk()
myWindow.geometry("420x400")
myWindow.title("menu principal du jeu")
f1=Frame(myWindow,bg='#41B77F')
f1.pack(expand=YES)
Labeltitle=Label(f1,text='menu du jeu saucisse',font=("arial",20),bg='#41B77F',fg='white')
Labeltitle.pack()
B=Button(f1,text='quitter',command=myWindow.destroy)
B.pack()
myWindow.config(background='#41B77F')
def open_window():
    Window=Tk()
B1=Button(f1,text='jouer',command=open_window)
B1.pack()
Labeltitle1=Label(f1,text='Preparez vous a jouer, regarder les regles et choississez votre couleur',font=("arial",8),bg='#41B77F',fg='white')
Labeltitle1.pack()

def change_color():
    colors=askcolor(title="Tkinter Color Chooser")
    myWindow.configure(bg=colors[1])

B3=Button(f1,text='Selectionner une couleur',command=change_color)
B3.pack()


myWindow.mainloop() 