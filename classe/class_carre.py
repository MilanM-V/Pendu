import pygame

class Carre:
    def __init__(self,ecran,x,y,largeur,hauteur,bg):
        """methode pour initialiser les parametre de la class Carre"""
        self.ecran=ecran
        self.x=x
        self.y=y
        self.largeur=largeur
        self.hauteur=hauteur
        self.bg=bg
        self.create_carre()
    
    def create_carre(self):
        """methode pour cree le carre"""
        self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
    def dessiner(self):
        """methode pour dessiner le carre"""
        pygame.draw.rect(self.ecran,self.bg, self.rect)