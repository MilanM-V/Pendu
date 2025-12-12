import pygame
from class_label import *

class ZoneDeTexte():
    def __init__(self,ecran,x,y,largeur,hauteur,couleurTexte,couleurFond,couleurBordure,tailleBordure,borderRadius=0,nbLettreMax=None,actif=True,desactivate=True,cara_excle=[],censure=False):
        self.ecran=ecran
        self.x=x
        self.y=y
        self.largeur=largeur
        self.hauteur=hauteur
        self.couleurTexte=couleurTexte
        self.couleurFondOriginal=couleurFond
        self.couleurFondAct=self.couleurFondOriginal
        self.couleurBordure=couleurBordure
        self.tailleBordure=tailleBordure
        self.borderRadius=borderRadius
        self.nbLettreMax=nbLettreMax
        self.actif=actif
        self.texte=""
        self.scrollX=0
        self.censure=censure
        self.desactivate=desactivate
        self.font = pygame.font.SysFont(None, self.hauteur-30)
        self.rect=pygame.Rect(x,y,self.largeur,self.hauteur)
        self.surface_texte=None
        self.caractereEnTrop=0
        self.warningShow=False
        self.waringTime=0
        self.cara_excle=cara_excle
        
        self.warningDuree=2000
        self.tailleMoyCharacter=self.font.size('A')[0]
        self.warningLabel=Label(self.ecran,"",(248, 250, 252),(self.rect.x+(self.rect.width//2),self.rect.y+self.rect.height+self.rect.height//2),"center",30,'transparent')
        self._updateTexteSurface()
        if self.desactivate:
            self._desactiver()
        
    def _updateTexteSurface(self):
        if self.censure:
            self.surface_texte = self.font.render("*"*len(self.texte), True, self.couleurTexte)
        else:
            self.surface_texte = self.font.render(self.texte, True, self.couleurTexte)
        
    def dessiner(self):
        bordure_rect=(self.x-self.tailleBordure,self.y-self.tailleBordure,self.largeur+2*self.tailleBordure,self.hauteur+2*self.tailleBordure)
        pygame.draw.rect(self.ecran,self.couleurBordure,bordure_rect,border_radius=self.borderRadius)
        pygame.draw.rect(self.ecran,self.couleurFondAct, self.rect)
        
        if self.desactivate:
            self.desactiverLabel.dessiner()


        self.ecran.blit(self.surface_texte,(self.rect.x+5-self.scrollX,self.rect.y+(self.hauteur-self.surface_texte.get_height())//2))

        
        if self.warningShow:
            time=pygame.time.get_ticks()
            if time-self.waringTime>self.warningDuree:
                self.warningShow=False
            else:
                self.warningLabel.dessiner()
    
    def changeText(self,texte):
        self.texte=texte
        self._updateTexteSurface()

    def addText(self,event):
        if not self.actif:
            return
        
        texteAvant=self.texte
        
        if event.key==pygame.K_BACKSPACE:
            if len(self.texte)>0:
                self.texte=self.texte[:-1]
        elif event.unicode.isprintable() and event.unicode in self.cara_excle:
            self.warningLabel.changer_texte(f"Vous ne pouvez pas rentrer ce type de caractere")

            self.warningShow=True
            self.waringTime=pygame.time.get_ticks()
        
        elif event.unicode.isprintable() and len(self.texte)<self.nbLettreMax:
            self.texte+=event.unicode
        elif event.unicode.isprintable():
            self.warningLabel.changer_texte(f"Vous ne pouvez rentrer que {self.nbLettreMax} caractere")

            self.warningShow=True
            self.waringTime=pygame.time.get_ticks()
       
            
            
        if self.texte!=texteAvant or event.key==pygame.K_BACKSPACE:
            self._updateTexteSurface()

        
    def checkClick(self,pos):
        if self.rect.collidepoint(pos) and not self.desactivate:
            self.actif=True
            r,g,b=self.couleurFondOriginal
            self.couleurFondAct=(r-50,g-50,b-50)
        else:
            self.couleurFondAct=self.couleurFondOriginal
            self.actif= False
            
    def _desactiver(self):
        x,y=self.rect.x+(self.rect.width//2),self.rect.y+(self.rect.height//4)
        self.desactiverLabel=Label(self.ecran,"Selectionner d'abord \nentre Lettre et Mot",(150, 150, 150),(x,y),"center",30,"transparent",ecartLigne=30)
        self.couleurFondAct=(200,200,200)
        self.desactivate=True
    def activate(self):
        self.desactivate=False
        self.couleurFondAct=self.couleurFondOriginal
            
            
class AfficheMots():
    def __init__(self,ecran,x,y,largeur,hauteur,nbLettre,couleurTexte):
        self.nbLettre=nbLettre
        self.x=x
        self.y=y
        self.ecran=ecran
        self.largeur=largeur
        self.hauteur=hauteur
        self.couleurTexte=couleurTexte
        self.font = pygame.font.SysFont(None,self.largeur//(self.nbLettre))
        self.mot="_ "+"_ "*(self.nbLettre-2)+"_"
        self.update_text_surface()
        
    def initialiseMot(self):
        self.mot="_ "+"_ "*(self.nbLettre-2)+"_"
        self.surface_texte=self.font.render(self.mot,True,self.couleurTexte)
    def update_text_surface(self):
        self.surface_texte=self.font.render(self.mot,True,self.couleurTexte)
    
    def dessiner(self):
        texteRect=self.surface_texte.get_rect()
        texteRect.x=self.x+(self.largeur-texteRect.width)//2
        texteRect.y=self.y+(self.hauteur-texteRect.height)//2
        self.ecran.blit(self.surface_texte,texteRect)
        
    def changeMot(self,mot):
        self.mot=mot
        self.update_text_surface()
        
