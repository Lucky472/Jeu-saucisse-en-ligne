import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

from tkinter import *
from math import sqrt
INITIAL=0
ACTIVE=1
INACTIVE=2
DEAD=-1

RADIUS = 15
XMIN = 20
YMIN = 20
X_AXIS_LENGTH = 9
Y_AXIS_LENGTH = 7
DIST = 50
WIDTHCANVAS = 2*XMIN + (X_AXIS_LENGTH-1)*DIST
HEIGHTCANVAS = 2*YMIN + (Y_AXIS_LENGTH-1)*DIST
HEIGHTMENU = WIDTHCANVAS//128
COLORCANVAS = "#EEEEEE"
COLORPOINT = "#416FEC"
SHINY = "#18D9E4"
COLORPLAYER1 = "#40A040"
COLORPLAYER2 = "#ed1111"
SAUSAGEWIDTH = 20
TEXTFONT = 30

class Client(ConnectionListener):
    def __init__(self, host, port, window):
        self.window = window
        self.Connect((host, port))

        self.state=INITIAL
        print("Client started")
        print("Ctrl-C to exit")
        
        
    def Network_initplayer(self,data):
        print("Enter your nickname: ")
        nickname=stdin.readline().rstrip("\n")
        self.nickname=nickname
        connection.Send({"action": "nickname", "nickname": nickname})
        print("Enter your color: ")
        self.color=stdin.readline().rstrip("\n")
        connection.Send({"action": "color" ,"color": self.color})

        
    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Loop(self):
        connection.Pump()
        self.Pump()

    def quit(self):
        self.window.destroy()
        self.state=DEAD
   
    def Network_start(self,data):
        self.state=data["state"]
        print("started")
        print(self.state)
   
    def Network_newPoint(self, data):
        """"
        (x,y)=data["newPoint"]
        self.window.white_board_canvas.create_oval(x-R,y-R,x+R,y+R, fill = self.other_color)
        self.window.white_board_canvas.update()
        self.state = ACTIVE
        """
    
    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    def Network_setactive(self,data):
        self.state = ACTIVE
    
    def Network_other_color(self,data):
        self.other_color = data["other_color"]
    
    def Network_add_clicked_point(self,data):
        #prend en data le tuple (i,j) coordonnées du point dans la matrice du jeu
        point = data["clicked_point"]
        self.game_show.add_other_point(point)


#########################################################

class ClientWindow(Tk):
    def __init__(self, host, port):
        Tk.__init__(self)
        self.client = Client(host, int(port), self)
        self.game_show = GameShow(self)
        """self.white_board_canvas = Canvas(self, width=WIDTH, height = HEIGHT,bg='white')
        self.white_board_canvas.pack(side=TOP)
        self.white_board_canvas.bind("<Button-1>",self.drawNewPoint)
        quit_but=Button(self,text='Quitter',command = self.client.quit)
        quit_but.pack(side=BOTTOM)
        """

    def drawNewPoint(self,evt):
        """
        print("clic")
        print(self.client.state)
        if self.client.state==ACTIVE:
            self.white_board_canvas.create_oval(evt.x-R,evt.y-R,evt.x+R,evt.y+R, fill = self.client.color )
            self.client.Send({"action":"newPoint","newPoint" : (evt.x,evt.y)})
            self.client.state = INACTIVE
            """
        pass

    def myMainLoop(self):
        while self.client.state!=DEAD:   
            self.update()
            self.client.Loop()
            sleep(0.001)
        exit()    

class GameShow:
    def __init__(self,window,client):
        #Initialise l'interface graphique
        self.window = window
        self.client = client
        #self.window.iconbitmap("IMAGE-SAUCISSE.ico")
        self.plateau = Frame(self.window,width=WIDTHCANVAS,height=HEIGHTCANVAS)
        self.menu = Frame(self.window,width=WIDTHCANVAS,height=HEIGHTMENU)
        self.canvas = Canvas(self.plateau, width = WIDTHCANVAS,height=HEIGHTCANVAS,bg=COLORCANVAS,highlightthickness=3,highlightbackground=COLORPOINT)
        self.game_engine = GameEngine(self.canvas)
        self.label_text_next_to_active_player = Label(self.menu, text="Active player:", bg=self.active_player_color(),font = TEXTFONT)
        self.active_player = StringVar()    
        self.active_player.set(self.game_engine.active_player)
        self.label_active_player = Label(self.menu,textvariable = self.active_player, bg=self.active_player_color(),font = TEXTFONT)
        self.button_forfeit = Button(self.menu, text='Forfeit', command = self.forfeit_popup)
        self.button_undo = Button(self.menu, text='Undo', command=self.reset_sausage)
        self.canvas.bind("<Button-1>",self.on_click)

        self.game_on = True

        #Pack l'interface graphique
        self.menu.pack(expand=YES,side=TOP)
        self.plateau.pack(expand=YES,side=BOTTOM)
        self.canvas.pack(expand=YES)
        self.label_active_player.pack(expand=YES,side=RIGHT)
        self.label_text_next_to_active_player.pack(side=RIGHT)
        self.button_forfeit.pack(side = LEFT)
        self.button_undo.pack(side=LEFT, padx=WIDTHCANVAS//3)
        self.draw_board()
    def active_player_color(self):
        if self.game_engine.active_player == self.game_engine.list_player[0]:
            return COLORPLAYER1
        if self.game_engine.active_player == self.game_engine.list_player[1]:
            return COLORPLAYER2
        
    def forfeit_popup(self):
        self.forfeit_popup = messagebox.askyesno(title='Forfeit', message='Do you really want to forfeit?')
        if self.forfeit_popup == YES:
            self.game_engine.change_active_player()
            self.active_player.set(self.game_engine.active_player)
            self.label_text_next_to_active_player["bg"]=self.active_player_color()
            self.label_active_player["bg"]=self.active_player_color()
            self.show_winner()
            self.canvas.after(3000,self.window.destroy)

        if self.forfeit_popup == NO:
            pass
        
    def draw_board(self):
        """
        parcours la liste de points et crossings et quand il y a un point, le dessine 
        """
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if self.game_engine.is_a_point(i,j):
                    self.game_engine.board[i][j].id = self.canvas.create_oval(XMIN+i*DIST-RADIUS,YMIN+j*DIST-RADIUS,XMIN+i*DIST+RADIUS,YMIN+j*DIST+RADIUS,fill = COLORPOINT)
        self.highlight_points()
                
    def on_click(self,evt):
        """
            S'occupe de tous les évéènements à appeller lors d'un clic
        """
        if self.game_on:
            self.game_engine.on_click(evt)
            if len(self.game_engine.selected_dots) == 3 :
                self.draw_sausage(self.game_engine.selected_dots)
                self.change_color_point()
                self.game_engine.draw_sausage()
                #vérifie si la partie est finie
                if self.game_engine.game_over_test():
                    self.show_winner()
                    self.game_on = False
                self.game_engine.change_active_player()
                self.active_player.set(self.game_engine.active_player)
                self.label_text_next_to_active_player["bg"]=self.active_player_color()
                self.label_active_player["bg"]=self.active_player_color()
            self.highlight_points()
            if len(self.game_engine.selected_dots) != 0 :
                dot_x, dot_y = self.game_engine.selected_dots[-1]
                self.color_point(self.game_engine.board[dot_x][dot_y],self.active_player_color())
    
    def add_other_point(self,point):
        if self.game_on:
             if len(self.game_engine.selected_dots) == 3 :
                self.draw_sausage(self.game_engine.selected_dots)
                self.change_color_point()
                self.game_engine.draw_sausage()
                #vérifie si la partie est finie
                if self.game_engine.game_over_test():
                    self.show_winner()
                    self.game_on = False
                self.game_engine.change_active_player()
                self.active_player.set(self.game_engine.active_player)
                self.label_text_next_to_active_player["bg"]=self.active_player_color()
                self.label_active_player["bg"]=self.active_player_color()
             self.highlight_points()
        if len(self.game_engine.selected_dots) != 0 :
                dot_x, dot_y = self.game_engine.selected_dots[-1]
                self.color_point(self.game_engine.board[dot_x][dot_y],self.active_player_color())




    def draw_sausage(self,dots):
        """
            Dessine la saucisse étant donné un tuple avec les coordonnés dans le tableau de 3 points
        """
        point1 = self.game_engine.canvas.coords(self.game_engine.board[dots[0][0]][dots[0][1]].id)
        point2 = self.game_engine.canvas.coords(self.game_engine.board[dots[1][0]][dots[1][1]].id)
        point3 = self.game_engine.canvas.coords(self.game_engine.board[dots[2][0]][dots[2][1]].id)

        if self.game_engine.active_player == self.game_engine.list_player[0] : 
            alpha = COLORPLAYER1 
        else : 
            alpha = COLORPLAYER2 

        if len(self.game_engine.selected_dots) ==3: 
            center1 = ((point1[2] + point1[0])/2,(point1[3] + point1[1])/2)
            center2 = ((point2[2] + point2[0])/2,(point2[3] + point2[1])/2)
            center3 = ((point3[2] + point3[0])/2,(point3[3] + point3[1])/2)

            self.canvas.create_line(center1[0],center1[1],center2[0],center2[1], fill= alpha, width=SAUSAGEWIDTH )
            self.canvas.create_line(center2[0],center2[1],center3[0],center3[1], fill= alpha, width=SAUSAGEWIDTH )
    
    def highlight_points(self):
        """
            Met en surbrillance les points pouvant être cliqués
        """
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if self.game_engine.is_a_point(i,j):
                    point = self.game_engine.board[i][j]
                    if point.can_be_clicked :
                        self.color_point(point,SHINY)
                    elif (i,j) in self.game_engine.selected_dots:
                        pass                    
                    elif not point.occupied :
                        self.color_point(point,COLORPOINT)
    
    def color_point(self,point,color):
        """
        change la couleur d'un point par la couleur donnée.
        """
        self.canvas.itemconfig(point.id,fill = color)
    
    def change_color_point(self):
        """
            change la couleur des points selctionnées en fonction du joueur"
        """
        for dot in self.game_engine.selected_dots:
            point = self.game_engine.board[dot[0]][dot[1]]
            if self.game_engine.active_player == self.game_engine.list_player[0]:
                self.color_point(point,COLORPLAYER1)
            if self.game_engine.active_player == self.game_engine.list_player[1]:
                self.color_point(point,COLORPLAYER2)            
    
    def reset_sausage(self):
        """
            fonction pour annuler une saucisse en cours de fabrication
        """
        for dot in self.game_engine.selected_dots:
            self.color_point(self.game_engine.board[dot[0]][dot[1]],COLORPOINT)
        self.game_engine.update_all_degree()
        self.game_engine.reset_sausage()
        self.highlight_points()

    def show_winner(self):
        self.canvas.create_text(WIDTHCANVAS//2,HEIGHTCANVAS//2,text="Victoire du "+str(self.active_player.get()),fill= "black",font=TEXTFONT,)


class GameEngine:
    def __init__(self,canvas,client):
        self.client = client
        self.canvas = canvas
        self.board = self.set_new_board()
        self.list_player = ["Joueur 1","Joueur 2"]
        self.active_player = self.list_player[0]
        self.selected_dots = []
        
    def on_click(self,evt):
        """
        si le point cliqué peut être sélectionné : sélectionne le point et le met dans selected dots
        """
        dot = self.check_coord_mouse(evt)
        if dot != None and dot not in self.selected_dots :
            if self.board[dot[0]][dot[1]].can_be_clicked ==True:
                self.selected_dots.append(dot)
                self.client.Send({"action":"add_clicked_point","clicked_point":dot})
        self.update_dots_clickability()
    
    def reset_sausage(self):
        self.selected_dots = []
        self.update_dots_clickability()
        
    def draw_sausage(self):
        """
            vérifie si la saucisse peut être dessinée et actualise les status des points
        """
        for dot in self.selected_dots:
            self.board[dot[0]][dot[1]].occupied = True
        if self.selected_dots[0][0] == self.selected_dots[1][0] :
            self.board[self.selected_dots[0][0]][(self.selected_dots[0][1]+self.selected_dots[1][1])//2].occupied = True
        if self.selected_dots[0][1] == self.selected_dots[1][1] :
            self.board[(self.selected_dots[0][0]+self.selected_dots[1][0])//2][self.selected_dots[0][1]].occupied = True
        if self.selected_dots[2][0] == self.selected_dots[1][0] :
            self.board[self.selected_dots[2][0]][(self.selected_dots[2][1]+self.selected_dots[1][1])//2].occupied = True
        if self.selected_dots[2][1] == self.selected_dots[1][1] :
            self.board[(self.selected_dots[2][0]+self.selected_dots[1][0])//2][self.selected_dots[2][1]].occupied = True
        self.selected_dots = []
        self.update_all_degree()
        self.update_dots_clickability()
        
    def update_dots_clickability(self):
        for dot_x in range(0,X_AXIS_LENGTH):
            for dot_y in range(0,Y_AXIS_LENGTH):
                if self.is_a_point(dot_x,dot_y):
                    self.update_dot_clickability(dot_x,dot_y)
    
    def update_dot_clickability(self,dot_x,dot_y):
        """
        teste si le point peut être séléctionné pour une saucisse et modifie l'attribut is_clickable correctement
        """
        if self.board[dot_x][dot_y].occupied :
            self.board[dot_x][dot_y].can_be_clicked = False
        elif (dot_x,dot_y) in self.selected_dots:
            self.board[dot_x][dot_y].can_be_clicked = False
        elif len(self.selected_dots) == 0:
            self.board[dot_x][dot_y].can_be_clicked = self.dot_next_to_degree_2(dot_x,dot_y)
        else :
            self.board[dot_x][dot_y].can_be_clicked = self.are_connectable(self.selected_dots[-1],(dot_x,dot_y))

    def are_connectable(self,dot1_coords,dot2_coords):
        """
        renvoie un booléen
        True si les deux points sont adjacents et si (si elle existe) l'intersection entre eux n'est pas occupée
        False sinon
        le premier point peut être occupé
        si le second est occupé, renvoie false
        """
        dot1_x,dot1_y = dot1_coords
        dot2_x,dot2_y = dot2_coords
        dot2 = self.board[dot2_x][dot2_y]
        if abs(dot1_x - dot2_x) > 2 or abs(dot1_y - dot2_y) > 2 :
            return False
        if abs(dot1_x - dot2_x) == 2 and abs(dot1_y - dot2_y) == 2 :
            return False
        if dot2.occupied :
            return False
        if dot1_coords[0] != dot2_coords[0] and dot1_coords[1] != dot2_coords[1]:
            return True
        if dot1_x == dot2_x :
            return not self.board[dot1_x][(dot1_y+dot2_y)//2].occupied
        if dot1_y == dot2_y :
            return not self.board[(dot1_x+dot2_x)//2][dot1_y].occupied
        return False

    def dot_next_to_degree_2(self,dot_x,dot_y):
        #regarde les points adjacents et vérifie si au moins l'un d'eux est de degrès 2
        for dot in self.accessible_neighbours(dot_x,dot_y):
            if self.board[dot[0]][dot[1]].degree > 1 :
                return True
        return False

    def neighbours(self,dot_x,dot_y):
        """
        renvoie un tuple contenant tous les points existants et étant proches du point en parametre
        pour ce faire teste chaque point proche
        """
        neighbours = []
        if dot_x + 2 < X_AXIS_LENGTH :
            neighbours.append((dot_x + 2, dot_y))
        if dot_y + 2 < Y_AXIS_LENGTH :
            neighbours.append((dot_x, dot_y + 2))
        if dot_x - 2 >= 0 :
            neighbours.append((dot_x - 2, dot_y))
        if dot_y - 2 >= 0 :
            neighbours.append((dot_x, dot_y - 2))
        if dot_x + 1 < X_AXIS_LENGTH and dot_y + 1 < Y_AXIS_LENGTH :
            neighbours.append((dot_x + 1, dot_y + 1))
        if dot_x + 1 < X_AXIS_LENGTH and dot_y - 1 >= 0 :
            neighbours.append((dot_x + 1, dot_y - 1))
        if dot_x - 1 >= 0 and dot_y + 1 < Y_AXIS_LENGTH :
            neighbours.append((dot_x - 1, dot_y + 1))
        if dot_x - 1 >= 0 and dot_y - 1 >= 0 :
            neighbours.append((dot_x - 1, dot_y - 1))
        return tuple(neighbours)

    def accessible_neighbours(self,dot_x,dot_y):
        """
        renvoie un tuple contenant les tuples de coordonnées des points accessibles depuis le point de coordonnées x,y
        (doit prendre en compte si le point est occupé ainsi que les intersections)
        renvoie tuple vide si pas de points accessibles
        """
        accessible = []
        for other_dot in self.neighbours(dot_x,dot_y):
            if self.are_connectable((dot_x,dot_y),other_dot):
                accessible.append(other_dot)
        return tuple(accessible)

    def set_new_board(self):
        #Créer le tableau 2D avec des points en i+j pair et crossing sinon, renvoie ce tabelau
        point = [[0 for j in range(Y_AXIS_LENGTH)] for i in range(X_AXIS_LENGTH)]

        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if self.is_a_point(i,j):
                    point[i][j] = Point()
                else:
                    point[i][j] = Crossing()
        return point

    def game_over_test(self):
        #teste si des coups sont encore possibles sur le plateau
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if self.is_a_point(i,j):
                    if self.board[i][j].can_be_clicked :
                        return False
        return True
    
    def update_degree(self,dot_x,dot_y):
        #calcule le degré ( points libres atteignables) autour du point
        self.board[dot_x][dot_y].degree = len(self.accessible_neighbours(dot_x, dot_y))
    
    def update_all_degree(self):
        #update degree pour chaque point 
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if self.is_a_point(i,j):
                    self.update_degree(i,j)
    
    def check_coord_mouse(self,evt):
        """
            vérifie si la souris clique sur un point et renvoie les coords du point si oui et None sinon
        """
        x = evt.x
        y = evt.y
        for i in range(0,X_AXIS_LENGTH):
            for j in range(0,Y_AXIS_LENGTH):
                if self.is_a_point(i,j):
                    point_coord = self.canvas.coords(self.board[i][j].id)
                    if self.is_in_point(x,y,point_coord):
                        return (i,j)
        return None

    def is_in_point(self,x,y,point_coord):
        """
            Calcule la norme euclidienne entre le centre du cercle et le point donné.
            Renvoie un booléen indiquant si le point est dans le ercle ou non
        """
        center_x = (point_coord[2] + point_coord[0])/2
        center_y = (point_coord[3] + point_coord[1])/2
        dist = sqrt((abs(x-center_x))**2 +(abs(y-center_y))**2)
        if dist <= RADIUS:
            return True
        return False
    
    def change_active_player(self):
        if self.active_player == self.list_player[0]:
            self.active_player = self.list_player[1]
        else :
            self.active_player = self.list_player[0]
        
    def is_a_point(self,i,j):
        if (i+j)%2 == 0:
            return True
        return False



class Point:
    def __init__(self):
        self.occupied = False
        self.degree = 0
        self.id = 0
        self.can_be_clicked = True


class Crossing:
    def __init__(self):
        self.occupied = False





# get command line argument of client, port
if len(sys.argv) != 2:
    print("Please use: python3", sys.argv[0], "host:port")
    print("e.g., python3", sys.argv[0], "localhost:31425")
    host, port = "localhost", "31425"
else:
    host, port = sys.argv[1].split(":")
client_window = ClientWindow(host, port)
client_window.myMainLoop()



