from class_fenetre import *
from class_bouton import *
from class_zoneTexte import*
from class_label import*
from class_image import*
from class_carre import*
from class_intro import*
from networkClient import*
import pygame
from random import*
from jeux import *
import time
import sys

class Gui:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.key.set_repeat(500, 30)
        self.largeur_ecran=1920
        self.longueur_ecran=1080
        self.gestionnaireFenetre=Fenetre(self.largeur_ecran,self.longueur_ecran,"Pendu",(15, 23, 42))
        self.ecran=self.gestionnaireFenetre.creer_fenetre()
        self.running=True
        self.fps=40
        self.horloge=pygame.time.Clock()
        self.elements=[]
        self.network_client=NetworkClient('54.37.158.60',65432,self)
        self.pendu=Jeux()
        self.fenetreManager=FenetreManager(self)
        self.choix=None
        self.fini=False
        self.showErreur=False
        self.iaOnCour=False
        self.mutli=False
        self.thx=""
        self.showErreurTime=0
        self.gameInitialiser=False
        self.showErreurDuree=2000
        with open('mot.txt', 'r') as f:
            self.contenu = f.readlines()
        
    def evenementManager(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
            if event.type==pygame.KEYDOWN:
                if event.unicode.isprintable():
                    self.thx+=event.unicode
                    if self.thx.lower()=="zach" or self.thx.lower()=="adnane":
                        pygame.mixer.music.load("./musique/Premier_Gaou.mp3")
                        pygame.mixer.music.set_volume(0.4)
                        pygame.mixer.music.play()
                else:
                    self.thx=""
                if event.key!=pygame.K_TAB:
                    for elem in self.elements:
                        if isinstance(elem,ZoneDeTexte):
                            elem.addText(event)
                if event.key==pygame.K_ESCAPE:
                    self.running=False
                if event.key==pygame.K_RETURN :
                    for elem in self.elements:
                        if isinstance(elem,ZoneDeTexte) and not elem.desactivate and self.fenetreManager.fenetreActuelle in ["Jeux solo","Jeux ia"]:
                            if not self.network_client.gameStart and elem.texte!="":
                                if self.choix=="Lettre" :
                                    if elem.texte not in self.pendu.listeLettreTest:
                                        self.pendu.listeLettreTest.append(elem.texte.lower())
                                        self.fenetreManager.lettreUtiliser.changer_texte(self.fenetreManager.lettreUtiliser.texte+f"- {elem.texte}\n")
                                    motIncomplet=self.pendu.show()
                                    self.fenetreManager.motCacher.mot=motIncomplet
                                    self.fenetreManager.motCacher.update_text_surface()
                                    elem.changeText('')
                            
                                if self.choix=="Mot":
                                    if self.pendu.coup(elem.texte.lower()):
                                        result=""
                                        for lettre in elem.texte:
                                            result+=f"{lettre} "
                                        self.fenetreManager.motCacher.mot=result
                                    else:
                                        motIncomplet=self.pendu.show()
                                        self.showErreur=True
                                        self.showErreurTime=pygame.time.get_ticks()
                                    elem.changeText('')
                                
                                self.fenetreManager.imagePendu.changeImage(f'./image/{11-self.pendu.nombreTentative}.png')
                                if self.pendu.nombreTentative==1:
                                    self.fenetreManager.result.changer_texte(f"Vous avez Perdu")
                                    self.fenetreManager.resultWord.changer_texte(f"Le mot été {self.pendu.motSecret}")
                                    self.fini=True
                                    self.elements=self.fenetreManager.elementDessiner()
                                if "_" not in self.fenetreManager.motCacher.mot :
                                    self.fenetreManager.result.changer_texte(f"Vous avez gagner en {11-self.pendu.nombreTentative} coup")
                                    self.fenetreManager.resultWord.changer_texte(f"Le mot été {self.pendu.motSecret}")
                                    self.fini=True
                                    self.elements=self.fenetreManager.elementDessiner()
                            elif elem.texte!="":
                                if self.choix=="Lettre" and self.network_client.gameStart:
                                    if elem.texte not in self.pendu.listeLettreTest:
                                        self.pendu.listeLettreTest.append(elem.texte.lower())
                                        self.fenetreManager.lettreUtiliser.changer_texte(self.fenetreManager.lettreUtiliser.texte+f"- {elem.texte}\n")
                                    self.network_client.addLettre(elem.texte)
                                    elem.changeText('')

                    
                if event.key==pygame.K_F11:
                    self.gestionnaireFenetre.fullscreen()
                    self.fenetreManager.actualiser()
            if event.type==pygame.MOUSEBUTTONDOWN:
                for elem in self.elements:
                    if isinstance(elem,ZoneDeTexte):
                        elem.checkClick(event.pos)
                    if isinstance(elem,Bouton):
                        elem.check_click(event.pos)
            if event.type==pygame.MOUSEBUTTONUP:
                for elem in self.elements:
                    if isinstance(elem,Bouton):
                        elem.check_click_action(event.pos)
    
    def quitter(self):
        self.running=False
    def retour(self):
        self.pendu.reset()
        self.fenetreManager.imagePendu.changeImage(f'./image/{11-self.pendu.nombreTentative}.png')
        self.fenetreManager.lettreUtiliser.changer_texte("Lettre utiliser:\n")
        self.fenetreManager.lettreUtiliserIa.changer_texte("Lettre utiliser:\n")
        self.fenetreManager.zoneMot.changeText('')
        self.fenetreManager.retourFenetre()
        self.elements=self.fenetreManager.elementDessiner()
        
    def home(self):
        self.pendu.reset()
        if self.mutli and self.network_client:
            self.mutli=False
            self.gameInitialiser=False
            self.network_client.gameStart=False
        self.fenetreManager.imagePendu.changeImage(f'./image/{11-self.pendu.nombreTentative}.png')
        self.fenetreManager.lettreUtiliser.changer_texte("Lettre utiliser:\n")
        self.fenetreManager.lettreUtiliserIa.changer_texte("Lettre utiliser:\n")
        self.fenetreManager.zoneMot.changeText('')
        self.fenetreManager.changeFenetre('Menu principale')
        self.elements=self.fenetreManager.elementDessiner()
    def win(self):
        self.fenetreManager.changeFenetre('Win')
        self.elements=self.fenetreManager.elementDessiner()
    def jeuSolo(self):
        self.pendu.motSecret=self.contenu[randint(0,len(self.contenu)-1)].strip()
        self.StartGame()
    def choixLettre(self):
        for elem in self.elements:
            r,g,b=self.fenetreManager.boutonLettre.couleurBase
            self.fenetreManager.boutonLettre.couleur=(r,g-50,b-50)
            self.fenetreManager.boutonMot.couleur=self.fenetreManager.boutonMot.couleurBase
            self.choix="Lettre"
            if isinstance(elem,(ZoneDeTexte)):
                elem.activate()
                elem.nbLettreMax=1
                elem.changeText('')
    
    def choixMot(self):
        for elem in self.elements:
            r,g,b=self.fenetreManager.boutonMot.couleurBase
            self.fenetreManager.boutonMot.couleur=(r,g-50,b-50)
            self.fenetreManager.boutonLettre.couleur=self.fenetreManager.boutonLettre.couleurBase
            self.choix="Mot"
            if isinstance(elem,(ZoneDeTexte)):
                elem.activate()
                elem.nbLettreMax=self.fenetreManager.motCacher.nbLettre
                elem.changeText('')
    def jeuDuo(self):
        self.fenetreManager.changeFenetre('Jeux duo')
        self.elements=self.fenetreManager.elementDessiner()
    def settingDuo(self):
        self.pendu.motSecret=self.fenetreManager.zoneMot.texte
        self.StartGame()             
    def StartGame(self):
        self.fenetreManager.changeFenetre('Jeux solo')
        self.fenetreManager.motCacher.nbLettre=len(self.pendu.motSecret)
        self.fenetreManager.motCacher.initialiseMot()
        self.elements=self.fenetreManager.elementDessiner()
        self.fenetreManager.boutonLettre.couleur=self.fenetreManager.boutonLettre.couleurBase
        self.fenetreManager.boutonMot.couleur=self.fenetreManager.boutonMot.couleurBase
        self.fenetreManager.labelStatus.changer_texte("")
        for elem in self.elements:
            if isinstance(elem,(ZoneDeTexte)):
                elem._desactiver()
                
    def startIa(self):
        if self.bot.contenu:
            lettre=self.bot.lettrePlusFrequente()
        else:
            lettre=self.bot.alphabet[0]
        self.bot.alphabet.remove(lettre)
        self.pendu.listeLettreTest.append(lettre)
        motIncomplet=self.pendu.show()
        result=""
        self.fenetreManager.motCacherIa.mot=motIncomplet
        self.fenetreManager.motCacherIa.update_text_surface()
        self.fenetreManager.lettreUtiliserIa.changer_texte(self.fenetreManager.lettreUtiliserIa.texte+f"- {lettre}\n")
        for lettre in motIncomplet:
            if lettre!=" ":
                result+=lettre
        if self.pendu.motSecret in self.contenu:
            self.bot.bonMot(result)
        self.fenetreManager.imagePenduIa.changeImage(f'./image/{11-self.pendu.nombreTentative}.png')
        if self.pendu.nombreTentative==1:
            time.sleep(0.2)
            self.fenetreManager.result.changer_texte(f"L'ia a Perdu")
            self.iaOnCour=False
            self.fini=True
        if "_" not in self.fenetreManager.motCacherIa.mot:
            self.fenetreManager.result.changer_texte(f"L'ia a gagner en {11-self.pendu.nombreTentative} coup\nLe mot été {self.pendu.motSecret}")
            self.fini=True
            self.iaOnCour=False
        if len(self.bot.contenu)==1 and self.pendu.coup(self.bot.contenu[0]):
            self.fenetreManager.result.changer_texte(f"L'ia a gagner en {11-self.pendu.nombreTentative} coup\nLe mot été {self.pendu.motSecret}")
            self.fini=True
            self.iaOnCour=False
        time.sleep(0.5)
    def jeuIa(self):
        self.pendu.motSecret=self.fenetreManager.zoneMotIA.texte
        self.fenetreManager.changeFenetre('Jeux Ia')
        self.elements=self.fenetreManager.elementDessiner()
        self.bot=Bot()
        self.bot.taillePareil(len(self.pendu.motSecret))
        self.iaOnCour=True
    def iaSetting(self):
        self.fenetreManager.changeFenetre('Ia setting')
        self.elements=self.fenetreManager.elementDessiner()
    def connectionMulti(self):
        self.fenetreManager.changeFenetre('Multi')
        self.elements=self.fenetreManager.elementDessiner()
        self.network_client.start()
        self.mutli=True
    def contenueManager(self):
        for elem in self.elements:
            elem.dessiner()
        if self.showErreur:
            time=pygame.time.get_ticks()
            if time-self.showErreurTime>self.showErreurDuree:
                self.showErreur=False
            else:
                self.fenetreManager.labelErreur.dessiner()
    
    def IntroScene(self):
        intro=IntroScene(self.largeur_ecran,self.longueur_ecran,"PENDU")
        running=True
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                intro.gestionBalance(event)
            intro.update()
            intro.draw(self.ecran)
            if intro.fini:
                running=False
            pygame.display.flip()
            self.horloge.tick(60)
        self.run_game()
            
    def run_game(self):
        self.elements=self.fenetreManager.elementDessiner()
        while self.running:
            if self.fini:
                self.win()
                self.fini=False
            if self.iaOnCour:
                self.startIa()
            if self.mutli:
                if self.network_client.gameStart and not self.gameInitialiser:
                    self.fenetreManager.motCacher.nbLettre=self.network_client.lenMot
                    self.fenetreManager.motCacher.initialiseMot()
                    self.fenetreManager.changeFenetre('Jeux solo')
                    self.elements=self.fenetreManager.elementDessiner()
                    self.gameInitialiser=True
                if self.network_client.timer:
                    self.fenetreManager.timerLabel.changer_texte(f"Temps avant le debut de la partie: {self.network_client.timer}sec")
                if self.network_client.nbJoueurServeur:
                    self.fenetreManager.nbJoueur.changer_texte(f"Nombre de joueur connecter: {self.network_client.nbJoueurServeur}")
            self.horloge.tick(self.fps)
           
            self.evenementManager()
            self.gestionnaireFenetre.dessiner()
            self.contenueManager()
            
            pygame.display.flip()

        pygame.quit()
        
        
class FenetreManager():
    def __init__(self,guiInstance):
        self.gui=guiInstance
        self.fenetreActuelle="Menu principale"
        self.fenetrePrecedente=[]
        self.elementParFenetre={}
        self.creeElementPerma()
        self.creeElementParFenetre()
        self.creeElementPresquePerma()
        self.creeLabelErreur()
    def changeFenetre(self,nouvelleFenetre):
        self.fenetrePrecedente.append(self.fenetreActuelle)
        self.fenetreActuelle=nouvelleFenetre
    def retourFenetre(self):
        if self.fenetrePrecedente:
            self.fenetreActuelle=self.fenetrePrecedente[-1]
            self.fenetrePrecedente.pop(-1)
    def actualiser(self):
        self.creeElementParFenetre()
        self.creeElementPerma()
        self.creeElementPresquePerma()
    def creeLabelErreur(self):
        self.labelErreur=Label(self.gui.ecran,"Ce n'est pas le bon mot",(248, 250, 252),(self.zone.warningLabel.x,self.zone.warningLabel.y),'center',30,"transparent")
    def creeElementPerma(self):
        self.elementPerma=[]
        boutonQuit=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct-60),(10),40,40,(15, 23, 42),'',bordure_taille=0,image="./image/quit.png",action=self.gui.quitter)
        self.elementPerma.append(boutonQuit)
    def creeElementPresquePerma(self):
        self.elementPresquePerma=[]
        boutonBack=Bouton(self.gui.ecran,(20),(10),60,60,(15, 23, 42),'',bordure_taille=0,image="./image/back.png",action=self.gui.retour)
        self.elementPresquePerma.append(boutonBack)
    def creeElementParFenetre(self):
        caracteres_speciaux = ['é', 'è', 'ê', 'ë', 'à', 'â', 'ä', 'ù', 'û', 'ü', 'ô', 'ö', 'î', 'ï', 'ç', 'É', 'È', 'Ê', 'Ë', 'À', 'Â', 'Ä', 'Ù', 'Û', 'Ü', 'Ô', 'Ö', 'Î', 'Ï', 'Ç', '.', ',', '!', '?', ';', ':', '(', ')', '[', ']', '{', '}', '"', "'", '+', '-', '*', '/', '%', '=', '<', '>', '#', '@', '&', '|', '\\', '$', '€', '£', '^', '`', '~', ' ',]
        menuPrincipalBouton=[]
        jeuxSolo=[]
        winScreen=[]
        jeuxDuo=[]
        jeuxMulti=[]
        jeuxIa=[]
        jeuxSettingIa=[]
        carre=Carre(self.gui.ecran,self.gui.gestionnaireFenetre.largeurAct*0.3958,self.gui.gestionnaireFenetre.hauteurAct*0.2222,
                    self.gui.gestionnaireFenetre.largeurAct*0.2083,self.gui.gestionnaireFenetre.hauteurAct*0.5555,(30, 41, 59))
        menuPrincipalBouton.append(carre)
        boutonSolo=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//2-self.gui.gestionnaireFenetre.largeurAct*0.0781),(self.gui.gestionnaireFenetre.hauteurAct//2-self.gui.gestionnaireFenetre.hauteurAct*0.0926)
                            ,300,75,(6, 182, 212),"👤 Jouer tout seul",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.jeuSolo,font="segoeuiemoji",font_size=25,border_radius=10)
        menuPrincipalBouton.append(boutonSolo)
        boutonDuo=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct/2-self.gui.gestionnaireFenetre.largeurAct*0.0781),(self.gui.gestionnaireFenetre.hauteurAct//2)
                        ,300,75,(6, 182, 212),"👥 Jouer à deux",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.jeuDuo,font="segoeuiemoji",font_size=25,border_radius=10)
        menuPrincipalBouton.append(boutonDuo)
        boutonIa=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct/2-self.gui.gestionnaireFenetre.largeurAct*0.0781),(self.gui.gestionnaireFenetre.hauteurAct//2+self.gui.gestionnaireFenetre.hauteurAct*0.0926)
                        ,300,75,(6, 182, 212),"🤖 Jouer contre une ia",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.iaSetting,font="segoeuiemoji",font_size=25,border_radius=10)
        menuPrincipalBouton.append(boutonIa)
        
        boutonMulti=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct/2-self.gui.gestionnaireFenetre.largeurAct*0.0781),(self.gui.gestionnaireFenetre.hauteurAct//2+200)
                        ,300,75,(51, 65, 85),"🌍 Jouer en multi\n(en cours de developpement)",couleur_texte=(100, 116, 139),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.connectionMulti,font="segoeuiemoji",font_size=20,border_radius=10)
        menuPrincipalBouton.append(boutonMulti)
        
        labelTitre=Label(self.gui.ecran,"Pendu",(6, 182, 212),(self.gui.gestionnaireFenetre.largeurAct//2,self.gui.gestionnaireFenetre.hauteurAct*0.2777),'center',50,'transparent')
        menuPrincipalBouton.append(labelTitre)
        
        labelSousTitre=Label(self.gui.ecran,"Choisissez votre mode de jeu",(148, 163, 184),(self.gui.gestionnaireFenetre.largeurAct//2,self.gui.gestionnaireFenetre.hauteurAct*0.34),'center',30,'transparent',font="Helvetica")
        menuPrincipalBouton.append(labelSousTitre)
        
        labelQuit=Label(self.gui.ecran,"Appuyez sur ECHAP pour quitter",(71, 85, 105),(self.gui.gestionnaireFenetre.largeurAct//2,self.gui.gestionnaireFenetre.hauteurAct*0.92),'center',25,'transparent',font="Arial")
        menuPrincipalBouton.append(labelQuit)
        
        self.zoneMot=ZoneDeTexte(ecran=self.gui.ecran,x=(self.gui.gestionnaireFenetre.largeurAct//2)-((self.gui.gestionnaireFenetre.largeurAct//12)),
                         y=self.gui.gestionnaireFenetre.hauteurAct/2-(self.gui.gestionnaireFenetre.hauteurAct//16),
                         largeur=self.gui.gestionnaireFenetre.largeurAct//6,hauteur=80,couleurTexte=(0,0,0),couleurFond=(200,200,200),couleurBordure=(0,0,0),tailleBordure=3,nbLettreMax=12,actif=True,desactivate=False,cara_excle=caracteres_speciaux,censure=True)
        jeuxDuo.append(self.zoneMot)    
        self.titre=Label(self.gui.ecran,"Rentrez le mot à deviner",(248, 250, 252),((self.gui.gestionnaireFenetre.largeurAct//2),self.gui.gestionnaireFenetre.hauteurAct//3),
                                   "center",50,"transparent",ecartLigne=60)
        jeuxDuo.append(self.titre)
        boutonValide=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct/2-round(self.gui.gestionnaireFenetre.largeurAct*0.0781)),(self.gui.gestionnaireFenetre.hauteurAct//2+self.gui.gestionnaireFenetre.hauteurAct//8)
                        ,round(self.gui.gestionnaireFenetre.largeurAct*0.0781)*2,100,(6, 182, 212),"Valider",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.settingDuo)
        jeuxDuo.append(boutonValide)
        
        self.zoneMotIA=ZoneDeTexte(ecran=self.gui.ecran,x=(self.gui.gestionnaireFenetre.largeurAct//2)-((self.gui.gestionnaireFenetre.largeurAct//12)),
                         y=self.gui.gestionnaireFenetre.hauteurAct/2-(self.gui.gestionnaireFenetre.hauteurAct//16),
                         largeur=self.gui.gestionnaireFenetre.largeurAct//6,hauteur=80,couleurTexte=(0,0,0),couleurFond=(200,200,200),couleurBordure=(0,0,0),tailleBordure=3,nbLettreMax=12,actif=True,desactivate=False,cara_excle=caracteres_speciaux)
        jeuxSettingIa.append(self.zoneMotIA)    
        self.titreIA=Label(self.gui.ecran,"Rentrez le mot à deviner",(248, 250, 252),((self.gui.gestionnaireFenetre.largeurAct//2),self.gui.gestionnaireFenetre.hauteurAct//3),
                                   "center",50,"transparent",ecartLigne=60)
        jeuxSettingIa.append(self.titreIA)
        boutonValideIA=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct/2-round(self.gui.gestionnaireFenetre.largeurAct*0.0781)),(self.gui.gestionnaireFenetre.hauteurAct//2+self.gui.gestionnaireFenetre.hauteurAct//8)
                        ,round(self.gui.gestionnaireFenetre.largeurAct*0.0781)*2,100,(6, 182, 212),"Valider",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.jeuIa)
        jeuxSettingIa.append(boutonValideIA)
        
        self.lettreUtiliserIa=Label(self.gui.ecran,"Lettre utiliser:\n",(248, 250, 252),(self.gui.gestionnaireFenetre.largeurAct//8,self.gui.gestionnaireFenetre.hauteurAct//3),
                                   "left",50,"transparent",ecartLigne=30)
        jeuxIa.append(self.lettreUtiliserIa)
        self.imagePenduIa=Image(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//4*3),self.gui.gestionnaireFenetre.hauteurAct//8,"./image/1.png",
                              "ajuster",self.gui.gestionnaireFenetre.largeurAct//6,self.gui.gestionnaireFenetre.largeurAct//3)
        jeuxIa.append(self.imagePenduIa)
        self.motCacherIa=AfficheMots(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//2)-((self.gui.gestionnaireFenetre.largeurAct//3)//2),self.gui.gestionnaireFenetre.hauteurAct//2,
                              self.gui.gestionnaireFenetre.largeurAct//3,round(self.gui.gestionnaireFenetre.hauteurAct*0.01852),5,(248, 250, 252))
        jeuxIa.append(self.motCacherIa)
        
        
        self.lettreUtiliser=Label(self.gui.ecran,"Lettre utiliser:\n",(248, 250, 252),(self.gui.gestionnaireFenetre.largeurAct//8,self.gui.gestionnaireFenetre.hauteurAct//3),
                                   "left",50,"transparent",ecartLigne=30)
        jeuxSolo.append(self.lettreUtiliser)
        self.imagePendu=Image(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//4*3),self.gui.gestionnaireFenetre.hauteurAct//8,"./image/1.png",
                              "ajuster",self.gui.gestionnaireFenetre.largeurAct//6,self.gui.gestionnaireFenetre.largeurAct//3)
        jeuxSolo.append(self.imagePendu)
        self.zone=ZoneDeTexte(ecran=self.gui.ecran,x=(self.gui.gestionnaireFenetre.largeurAct//2)-((self.gui.gestionnaireFenetre.largeurAct//12)),
                         y=self.gui.gestionnaireFenetre.hauteurAct-(self.gui.gestionnaireFenetre.hauteurAct/3),
                         largeur=self.gui.gestionnaireFenetre.largeurAct//6,hauteur=80,couleurTexte=(0,0,0),couleurFond=(200,200,200),couleurBordure=(0,0,0),tailleBordure=3,cara_excle=caracteres_speciaux)
        jeuxSolo.append(self.zone)        
        self.motCacher=AfficheMots(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//2)-((self.gui.gestionnaireFenetre.largeurAct//3)//2),self.gui.gestionnaireFenetre.hauteurAct//5,
                              self.gui.gestionnaireFenetre.largeurAct//3,round(self.gui.gestionnaireFenetre.hauteurAct*0.01852),5,(248, 250, 252))
        jeuxSolo.append(self.motCacher)
        self.boutonLettre=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//2+(self.gui.gestionnaireFenetre.largeurAct//66)),
                            (self.gui.gestionnaireFenetre.hauteurAct//2)
                        ,self.gui.gestionnaireFenetre.largeurAct//6,(self.gui.gestionnaireFenetre.hauteurAct//10),(6, 182, 212),"Lettre",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.choixLettre)
        jeuxSolo.append(self.boutonLettre)
        self.boutonMot=Bouton(self.gui.ecran,(self.gui.gestionnaireFenetre.largeurAct//2-self.gui.gestionnaireFenetre.largeurAct//5.5),
                         (self.gui.gestionnaireFenetre.hauteurAct//2)
                        ,self.gui.gestionnaireFenetre.largeurAct//6,(self.gui.gestionnaireFenetre.hauteurAct//10),(6, 182, 212),"Mot",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.choixMot)
        jeuxSolo.append(self.boutonMot)
        self.labelStatus = Label(self.gui.ecran, "", (6, 182, 212), (self.gui.gestionnaireFenetre.largeurAct // 2, self.gui.gestionnaireFenetre.hauteurAct * 0.12), 'center', 40, 'transparent')
        jeuxSolo.append(self.labelStatus)
        labelTuto=Label(self.gui.ecran,"Appuyez sur ENTREE pour valider la lettre ou le mot",(71, 85, 105),(self.gui.gestionnaireFenetre.largeurAct//2,self.gui.gestionnaireFenetre.hauteurAct*0.92),'center',25,'transparent',font="Arial")
        jeuxSolo.append(labelTuto)
        self.result=Label(self.gui.ecran,f"Vous avez gagner en {self.gui.pendu.nombreTentative} coup",(248, 250, 252),(self.gui.gestionnaireFenetre.largeurAct//2,
                                                                                                             self.gui.gestionnaireFenetre.hauteurAct//2-self.gui.gestionnaireFenetre.hauteurAct*0.1),'center',70,'transparent')
        winScreen.append(self.result)
        self.resultWord=Label(self.gui.ecran,f"Le mot été",(248, 250, 252),(self.gui.gestionnaireFenetre.largeurAct//2,
                                                                                                             self.gui.gestionnaireFenetre.hauteurAct//2+self.gui.gestionnaireFenetre.hauteurAct*0.05),'center',70,'transparent')
        winScreen.append(self.resultWord)
        homeBoutton=Bouton(self.gui.ecran,self.gui.gestionnaireFenetre.largeurAct/2-round(self.gui.gestionnaireFenetre.largeurAct*0.0781),(self.gui.gestionnaireFenetre.hauteurAct//2+(self.gui.gestionnaireFenetre.hauteurAct//6)),round(self.gui.gestionnaireFenetre.largeurAct*0.0781)*2
                           ,self.gui.gestionnaireFenetre.hauteurAct//8,(6, 182, 212),"Menu principale",couleur_texte=(15, 23, 42),bordure_taille=5,couleur_bordure=(0,0,0),action=self.gui.home)
        winScreen.append(homeBoutton)
        self.timerLabel=Label(self.gui.ecran,"Temps avant le debut de la partie: ??sec","White",(self.gui.gestionnaireFenetre.largeurAct//2,self.gui.gestionnaireFenetre.hauteurAct*0.7),'center',50,'transparent')
        jeuxMulti.append(self.timerLabel)
        self.nbJoueur=Label(self.gui.ecran,"Nombre de joueur connecter: 0","White",(self.gui.gestionnaireFenetre.largeurAct//2,self.gui.gestionnaireFenetre.hauteurAct*0.5),'center',50,'transparent')
        jeuxMulti.append(self.nbJoueur)
        self.elementParFenetre['Menu principale']=menuPrincipalBouton
        self.elementParFenetre['Jeux solo']=jeuxSolo
        self.elementParFenetre['Win']=winScreen
        self.elementParFenetre['Jeux duo']=jeuxDuo
        self.elementParFenetre['Jeux Ia']=jeuxIa
        self.elementParFenetre['Ia setting']=jeuxSettingIa
        self.elementParFenetre['Multi']=jeuxMulti
    def elementDessiner(self):
        result=self.elementParFenetre.get(self.fenetreActuelle,[])
        result+=self.elementPerma
        if self.fenetreActuelle!="Menu principale":
            result+=self.elementPresquePerma
        return result