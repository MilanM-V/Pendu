import pygame

class Image():
    def __init__(self,ecran,x,y,lien,taille="remplir",largeur=None,hauteur=None):
        """methode pour initialiser les parametre de la class Image"""
        self.ecran=ecran
        self.x=x
        self.y=y
        self.taille=taille
        self.lien=lien
        self.largeur=largeur
        self.hauteur=hauteur
        self.image_surface=None
        self.creeImage()
    
    def creeImage(self):
        """methode pour creer l'image"""
        try:
            self.image_surface = pygame.image.load(self.lien).convert_alpha()
            if self.taille == "ajuster" and self.largeur and self.hauteur:
                self.image_surface = pygame.transform.scale(self.image_surface,(int(self.largeur),int(self.hauteur)))
        except :
            w=int(self.largeur) if self.largeur else 100
            h=int(self.hauteur) if self.hauteur else 100
            self.image_surface=pygame.Surface((w,h))
            self.image_surface.fill((100,100,100))
        
    def dessiner(self):
        """methode pour dessiner l'image"""
        if self.image_surface:
            try:
                self.ecran.blit(self.image_surface, (self.x, self.y))
            except pygame.error:
                pass 
        
    def changeImage(self,lien):
        """methode pour changer l'image"""
        self.lien=lien
        self.creeImage()