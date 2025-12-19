import pygame
from classe.class_fenetre import *



class Label:
    def __init__(self,ecran,texte,couleur,position,aligner_texte,taille_police,couleur_fond,font=None,ecartLigne=50):
        """methode pour initialiser les parametre de la fonction Label"""
        self.ecran=ecran
        self.texte=texte
        self.couleur=couleur
        self.x,self.y=position
        self.aligner_texte=aligner_texte
        self.taille_police=taille_police
        self.couleur_fond=couleur_fond
        self.ecartLigne=int(ecartLigne*ecran.get_height()/1080)
        if font and font.endswith(".ttf"): 
            self.fond=pygame.font.Font(font, int(self.taille_police*ecran.get_height()/1080))
        else:  
            self.fond=pygame.font.SysFont(font, int(self.taille_police*ecran.get_height()/1080))
        self.lignes=self.texte.split('\n')
        self.images=[]
        self.zone_textes=[]
        self.afficher=True
        for ligne in range(len(self.lignes)):
            #gerer si le fond du label est rtansparent ou pas
            if self.couleur_fond=='transparent':
                self.image=self.fond.render(self.lignes[ligne], True, self.couleur)
                self.image.convert_alpha()
            else:
                self.image=self.fond.render(self.lignes[ligne], True, self.couleur, self.couleur_fond)
            self.images.append(self.image)
            self.zone_texte=self.image.get_rect()
            #gerer ou on alligne le texte
            if self.aligner_texte=="center":
                self.zone_texte.center=(self.x,self.y+ligne*self.ecartLigne)
            elif self.aligner_texte=="left":
                self.zone_texte.topleft=(self.x,self.y+ligne*self.ecartLigne)
            elif self.aligner_texte=="right":
                self.zone_texte.topright=(self.x,self.y+ligne*self.ecartLigne)
            self.zone_textes.append(self.zone_texte)

    def changer_texte(self, nouveau_texte):
        #methode pour changer le texte du label
        self.texte=nouveau_texte
        self.lignes=self.texte.split('\n')
        self.images=[]
        self.zone_textes=[]
        self.afficher=True
        for ligne in range(len(self.lignes)):
            if self.couleur_fond=='transparent':
                self.image=self.fond.render(self.lignes[ligne],True,self.couleur)
                self.image.convert_alpha()
            else:
                self.image=self.fond.render(self.lignes[ligne],True,self.couleur,self.couleur_fond)
            self.images.append(self.image)
            self.zone_texte=self.image.get_rect()
            
            if self.aligner_texte=="center":
                self.zone_texte.center=(self.x, self.y+ligne*self.ecartLigne)
            elif self.aligner_texte=="left":
                self.zone_texte.topleft=(self.x,self.y+ligne*self.ecartLigne)
            elif self.aligner_texte=="right":
                self.zone_texte.topright = (self.x,self.y+ligne*self.ecartLigne)
            self.zone_textes.append(self.zone_texte)

    def dessiner(self):
        #methode pour afficher le labbel
        if self.afficher:
            for element in range(len(self.images)):
                self.ecran.blit(self.images[element], self.zone_textes[element])
            
    def supprimer_label(self):
        #methode pour supprimer le label
        self.afficher=False
        self.ecran.fill((0, 0, 0))


 