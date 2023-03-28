
import MyFirstClient as MFC
from tkinter import*
from tkinter.colorchooser import askcolor

host, port = "localhost", "31425"
nickname = "nick"
color = "#000865"

def open_window():
    client_window = MFC.ClientWindow(host, port,color,nickname)
    client_window.myMainLoop()
    
def change_color():
    colors=askcolor(title="Tkinter Color Chooser")
    myWindow.configure(bg=colors[1])
    color = colors[1]

#enregistrer pseudo dans une variable
def enregistrer_pseudo():
    nickname=pseudo_entry1.get()

def enregistrer_host():
    host=pseudo_entry2.get()
    
def enregistrer_port():
    port=pseudo_entry3.get()



myWindow=Tk()
myWindow.geometry("520x500")
myWindow.title("menu principal du jeu")
myWindow.config(background='#41B77F')

f1=Frame(myWindow,bg='#41B77F')
f1.pack(expand=YES)

Labeltitle1=Label(f1,text='Menu du jeu saucisse',font=("arial",30),bg='#41B77F',fg='white')
Labeltitle1.pack()

B1=Button(myWindow,text='quitter',command=myWindow.destroy,bg='#ed1111')
B1.pack(side=LEFT)


Labeltitle2=Label(f1,text='Preparez vous à jouer, regarder les règles et choississez votre couleur',font=("arial",10),bg='#41B77F',fg='white')
Labeltitle2.pack()


B2=Button(f1,text='Selectionner une couleur',command=change_color,bg='#4065A4')
B2.pack()


#pseudo
L3=Label(f1,text='choisi ton pseudo',font=("arial",19),bg='#41B77F',fg='white')
L3.pack()

f2= Frame(f1,bg='#41B77F')
pseudo_entry1=Entry(f2,font=("arial",20),bg='#41B77F',fg='white')
pseudo_entry1.pack()
f2.pack()

B3=Button(f1,text='valider',command=enregistrer_pseudo,bg='#4065A4')
B3.pack()



#host
L4=Label(f1,text='host',font=("arial",19),bg='#41B77F',fg='white')
L4.pack()

f3= Frame(f1,bg='#41B77F')
pseudo_entry2=Entry(f3,font=("arial",20),bg='#41B77F',fg='white')
pseudo_entry2.pack()
f3.pack()

B4=Button(f1,text='valider',command=enregistrer_host,bg='#4065A4')
B4.pack()

#port
L5=Label(f1,text='port',font=("arial",19),bg='#41B77F',fg='white')
L5.pack()

f4= Frame(f1,bg='#41B77F')
pseudo_entry3=Entry(f4,font=("arial",20),bg='#41B77F',fg='white')
pseudo_entry3.pack()
f4.pack()

B5=Button(f1,text='valider',command=enregistrer_port,bg='#4065A4')
B5.pack()


#bouton jouer
B6=Button(myWindow,text='   Jouer   ',command=open_window,bg='#4065A4')
B6.pack(side=BOTTOM)


myWindow.mainloop() 





    #changé arguments client: rajouté color et nickname
"""
    class Client(ConnectionListener):
        def __init__(self, host, port, window,color,nickname):
            self.window = window
            self.Connect((host, port))
            self.color = color
            self.nickname = nickname
            self.oponent_color = "#f3f300"
            self.state=INITIAL
            print("Client started")
            print("Ctrl-C to exit")
            
    class ClientWindow(Tk):
        def __init__(self, host, port,color,nickname):
            Tk.__init__(self)
            self.client = Client(host, int(port), self,color,nickname)
            self.game_show = GameShow(self,self.client)
    
    retirer ce qui suit dans myfirstclient:
        
    client_window = ClientWindow(host, port)
    client_window.myMainLoop()"""
"""
    