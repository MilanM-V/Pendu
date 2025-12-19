import asyncio
import websockets
import threading
import json


class NetworkClient:
    def __init__(self,ip,port,gui):
        """methode pour initialiser les parametre de la class NetworkClient"""
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
        """methode pour ajouter une letre a la liste des letre jouer"""
        self.lettre.append(lettre)
        self.show=True        
        
    async def sendeMessage(self,websocket):
        """methode pour envoyer les info (lettre jouer) au serveur"""
        while True:
            if self.show:
                payload=json.dumps({"lettre_test":self.lettre[-1]})
                await websocket.send(payload)
                self.show=False
            await asyncio.sleep(0.05)
    async def receiver(self, websocket):
        """methode pour recevoir les info du serveur et mettre a jour le jeu en consequence"""
        while True:
            message=await websocket.recv()
            try:
                message=json.loads(message)
            except:
                pass
            if isinstance(message, dict):
                if 'tempsRestant' in message:#recevoir le temps restant avant le depart de la partie
                    self.timer=message['tempsRestant']
                if "nbJoueur" in message:#recevoir le nombre de joueur dans la partie
                    self.nbJoueurServeur=message['nbJoueur']
                if message.get('type')=='gameStart': #recevoir le debut de la aprtie
                    self.lenMot=message['lenMot']
                    self.gameStart = True
                    self.gui.fini=False
                    self.gui.multiStart=True
                if message.get('type')=="updatePerso": #recevoir sont update apres avoir envoyer la lettre jouer et metrte a jour le jeu
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
                if message.get('type')=='elimination':#recevoir si on est eliminer
                    self.gui.fenetreManager.result.changer_texte(message.get('reason', f"Vous etes eliminer round {self.nbRound}"))
                    self.gui.fini=True
                    self.gui.multiStart=False
                if message.get('type')=="nouveau_round":#recevoir un nouveau round et reset le jeu
                    print(f"Round {message.get('round')}")
                    self.nbRound=message.get('round',self.nbRound)
                    self.gui.pendu.reset()
                    self.gui.fenetreManager.lettreUtiliser.changer_texte("Lettre utiliser:\n")
                    self.gui.fenetreManager.labelStatus.changer_texte("")
                    self.gui.fenetreManager.labelNbJoueur.changer_texte(f"Joueur restant: {message.get('nbJoueur')}")
                    self.gui.gameInitialiser=False
                    self.gui.fini=False
                    self.lenMot=message['lenMot']
                    self.gameStart=True
                if message.get('type')=="fin":#recevoir le gagnant
                    result=message.get('result')
                    winner=message.get('gagnant')
                    self.gui.multiStart=False
                    if result=='win':
                        self.gui.fenetreManager.result.changer_texte(f"VICTOIRE ! Vous avez gagné !")
                    else:
                        self.gui.fenetreManager.result.changer_texte(f"Défaite. Gagnant : {winner}")
                    self.gui.fini=True
                    self.gameStart=False

    async def run(self):
        """methode pour lancer le online"""
        try:
            async with websockets.connect(self.uri,open_timeout=5) as websocket:
                await websocket.send('join_game')
                receiver_task=asyncio.create_task(self.receiver(websocket))
                sender_task=asyncio.create_task(self.sendeMessage(websocket))
                await asyncio.gather(receiver_task, sender_task)
        except Exception as e:
            print("Erreur :", e)
    
    def start(self):
        """methode pour lancer la class dans un autre thread"""
        def _start_loop():
            self.loop=asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.run())

        thread=threading.Thread(target=_start_loop,daemon=True)
        thread.start()
