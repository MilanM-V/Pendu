import asyncio
import websockets
import threading
import json


class NetworkClient:
    def __init__(self,ip,port,gui):
        self.ip=ip
        self.port=port
        self.uri=f"ws://{self.ip}:{self.port}"
        self.loop = None
        self.lenMot=None
        self.timer=None
        self.gui=gui
        self.nbJoueurServeur=None
        self.gameStart=False
        self.show=False
        self.lettre=[]
        self.scoreboard=None
        self.nbRound=1
                
    def addLettre(self,lettre):
        self.lettre.append(lettre)
        self.show=True        
        
    async def sendeMessage(self,websocket):
        while True:
            if self.show:
                payload=json.dumps({"lettre_test":self.lettre[-1]})
                await websocket.send(payload)
                self.show=False
            await asyncio.sleep(0.05)
    async def receiver(self, websocket):
        while True:
            message=await websocket.recv()
            try:
                message=json.loads(message)
            except:
                pass
            if isinstance(message, dict):
                if 'tempsRestant' in message:
                    self.timer=message['tempsRestant']
                if "nbJoueur" in message:
                    self.nbJoueurServeur=message['nbJoueur']
                if message.get('type')=='gameStart' :
                    self.lenMot=message['lenMot']
                    self.gameStart = True
                    self.gui.fini=False
                if message.get('type')=="updatePerso":
                    motIncomplet=message['motIncomplet']
                    nbCoup=message["nbCoup"]
                    elimine=message['elimine']
                    gagne=message['gagne']
                    self.gui.fenetreManager.motCacher.changeMot(motIncomplet) 
                    self.gui.fenetreManager.imagePendu.changeImage(f'./image/{11-nbCoup}.png')
                    if elimine:
                        self.gui.fenetreManager.result.changer_texte(f"Vous etes eliminer round {self.nbRound}")
                        self.gui.fini=True
                    elif gagne:
                        self.gui.fenetreManager.labelStatus.changer_texte(f"Mot trouvé en {11-nbCoup} coups ! Attente des autres...")
                if message.get('type')=='elimination':
                    self.gui.fenetreManager.result.changer_texte(message.get('reason', f"Vous etes eliminer round {self.nbRound}"))
                    self.gui.fini=True
                if message.get('type')=="nouveau_round":
                    print(f"Round {message.get('round')}")
                    self.nbRound=message.get('round',self.nbRound)
                    self.gui.pendu.reset()
                    self.gui.fenetreManager.lettreUtiliser.changer_texte("Lettre utiliser:\n")
                    self.gui.fenetreManager.labelStatus.changer_texte("")
                    self.gui.gameInitialiser=False
                    self.gui.fini=False
                    self.lenMot=message['lenMot']
                    self.gameStart=True
                if message.get('type')=="fin":
                    result=message.get('result')
                    winner=message.get('gagnant')
                    if result=='win':
                        self.gui.fenetreManager.result.changer_texte(f"VICTOIRE ! Vous avez gagné !")
                    else:
                        self.gui.fenetreManager.result.changer_texte(f"Défaite. Gagnant : {winner}")
                    self.gui.fini=True
                    self.gameStart=False

    async def run(self):
        try:
            async with websockets.connect(self.uri,open_timeout=5) as websocket:
                await websocket.send('join_game')
                receiver_task=asyncio.create_task(self.receiver(websocket))
                sender_task=asyncio.create_task(self.sendeMessage(websocket))
                await asyncio.gather(receiver_task, sender_task)
        except Exception as e:
            print("Erreur :", e)
    
    def start(self):
        def _start_loop():
            self.loop=asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.run())

        thread=threading.Thread(target=_start_loop,daemon=True)
        thread.start()
