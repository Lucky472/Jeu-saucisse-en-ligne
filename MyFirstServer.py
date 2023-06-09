import sys
from time import sleep, localtime

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

ACTIVE = 1
INACTIVE = 2

class ClientChannel(Channel):
    """
    This is the server representation of a connected client.
    """
    nickname = "anonymous"
    
    def Close(self):
        self._server.DelPlayer(self)
    
    def Network_nickname(self, data):
        self.nickname = data["nickname"]
        self._server.PrintPlayers()
        self._server.start_player(data)
        
    def Network_color(self,data):
        self.color = data["color"]
        self._server.SendToOthers({"action":"other_color","other_color":self.color, "who":self.nickname})

    def Network_new_sausage(self,data):
        self._server.SendToOthers({"action":"oponent_played","sausage":data["sausage"], "who":self.nickname})

    def Network_forfeit(self,data):
        self._server.SendToOthers({"action":"oponent_forfeit", "who":self.nickname})
        
class MyServer(Server):
    channelClass = ClientChannel
    def __init__(self, mylocaladdr):
        Server.__init__(self, localaddr=mylocaladdr)
        self.players={}
        print('Server launched')
        self.pifpaf = True
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        print("New Player connected")
        self.players[player] = True
        if len(self.players) == 2 :
            self.send_to_all({"action": "initplayer"})
        
    def start_player(self,data):
        #[p.Send({"action": "initplayer"}) for p in self.players]
        if self.pifpaf :
            [p.Send({"action":"start","state":ACTIVE}) for p in self.players if p.nickname == data["nickname"]]
            print("pif")
        else :
            [p.Send({"action":"start","state":INACTIVE}) for p in self.players if p.nickname == data["nickname"]]
            print("paf")
        self.pifpaf = not self.pifpaf


    def PrintPlayers(self):
        print("players' nicknames :",[p.nickname for p in self.players])
  
    def DelPlayer(self, player):
        print("Deleting Player " + player.nickname + " at "+str(player.addr))
        del self.players[player]
       
    def SendToOthers(self, data):
        #p.send(data)
        [p.Send(data) for p in self.players if p.nickname != data["who"]]
    
    def sendto(self, data):
        [p.Send(data) for p in self.players if p.nickname == data["who"]]
    
    def send_to_all(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Please use: python3", sys.argv[0], "host:port")
    print("e.g., python3", sys.argv[0], "localhost:31425")
    host, port = "localhost","31425"
else:
    host, port = sys.argv[1].split(":")
s = MyServer((host, int(port)))
s.Launch()
