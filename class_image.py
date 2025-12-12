import pygame


class Image():
    def __init__(self,ecran,x,y,lien,taille="remplir",largeur=None,hauteur=None):
        self.ecran=ecran
        self.x=x
        self.y=y
        self.taille=taille
        self.lien=lien
        self.largeur=largeur
        self.hauteur=hauteur
        self.creeImage()
    
    def creeImage(self):
        self.image_surface = pygame.image.load(self.lien).convert_alpha()
        if self.taille=="ajuster":
            self.image_surface = pygame.transform.scale(self.image_surface, (self.largeur,self.hauteur))
        
        
    def dessiner(self):
        self.ecran.blit(self.image_surface,(self.x,self.y))
        
    def changeImage(self,lien):
        self.lien=lien
        self.creeImage()