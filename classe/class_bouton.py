import pygame


class Bouton:
    def __init__(self,ecran, x, y, largeur, hauteur, couleur, texte,action=None, couleur_texte=(0,0,0), echelle=1, bordure_taille=5, couleur_bordure=(255, 255, 255),border_radius=5,font_size=40,image=None,font=None):
        """initialisation des parametre de la class Bouton"""
        self.x=x
        self.y=y
        self.largeur=int(largeur*echelle)
        self.hauteur=int(hauteur*echelle)
        self.couleur=couleur
        self.couleurBase=couleur
        self.texte=texte.split("\n")
        self.couleur_texte=couleur_texte
        self.action=action
        self.image=image
        if self.image:
            self.image_surface=pygame.image.load(self.image).convert_alpha()
            self.image_surface=pygame.transform.scale(self.image_surface,(self.largeur,self.hauteur))
        self.rect=pygame.Rect(x,y,self.largeur,self.hauteur)
        self.bordure_taille_start=bordure_taille
        self.bordure_taille=bordure_taille
        self.couleur_bordure=couleur_bordure
        self.font=pygame.font.SysFont(font,int(font_size*ecran.get_height()/1080))
        self.border_radius=border_radius
        self.boutonPresse=False
        self.ecran=ecran

    def dessiner(self):
        #methode pour faire afficher les bouton
        if self.boutonPresse:
            self.bordure_taille=self.bordure_taille_start-2
        
        bordure_rect=(self.x-self.bordure_taille,self.y-self.bordure_taille,self.largeur+2*self.bordure_taille,self.hauteur+2*self.bordure_taille)
        pygame.draw.rect(self.ecran,self.couleur_bordure,bordure_rect,border_radius=self.border_radius)
        pygame.draw.rect(self.ecran,self.couleur,self.rect,border_radius=self.border_radius)

        if self.image:
            texte_rect=self.image_surface.get_rect(center=self.rect.center)
            self.ecran.blit(self.image_surface,texte_rect)
        else:
            ligne=0
            for text in self.texte:
                texte_surface = self.font.render(text, True, self.couleur_texte)
                texte_rect = texte_surface.get_rect(center=self.rect.center)
                if len(self.texte)>1:
                    x,y,l,h=texte_rect
                    self.ecran.blit(texte_surface,(x,y+(ligne*30)-(h//2),l,h))
                    ligne+=1
                else:
                    self.ecran.blit(texte_surface,(texte_rect))
    def changer_texte(self,text):
        #methode pour changer le texte des boutons
        self.texte=text.split("\n")

    def check_click(self, pos):
        #methode pour verifier si le bouton est cliquer
        if self.rect.collidepoint(pos):
            self.boutonPresse=True  
            return True
        return False
    def check_click_action(self,pos):
        "methode pour verifier si un bouton est appuyer et executer sa fonction"
        self.boutonPresse=False
        self.bordure_taille=self.bordure_taille_start
        if self.rect.collidepoint(pos):
            if self.action is not None and callable(self.action):
                self.action()

