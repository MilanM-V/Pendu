import pygame

class Image():
    def __init__(self, ecran, x, y, lien, taille="remplir", largeur=None, hauteur=None):
        self.ecran = ecran
        self.x = x
        self.y = y
        self.taille = taille
        self.lien = lien
        self.largeur = largeur
        self.hauteur = hauteur
        self.image_surface = None  # ✅ Initialisation importante
        self.creeImage()
    
    def creeImage(self):
        try:
            self.image_surface = pygame.image.load(self.lien).convert_alpha()
            if self.taille == "ajuster" and self.largeur and self.hauteur:
                self.image_surface = pygame.transform.scale(
                    self.image_surface, 
                    (int(self.largeur), int(self.hauteur))
                )
        except (pygame.error, FileNotFoundError, OSError) as e:
            print(f"⚠️  Erreur chargement image '{self.lien}': {e}")
            # Créer une surface de secours
            w = int(self.largeur) if self.largeur else 100
            h = int(self.hauteur) if self.hauteur else 100
            self.image_surface = pygame.Surface((w, h))
            self.image_surface.fill((100, 100, 100))  # Gris foncé
        
    def dessiner(self):
        if self.image_surface:  # ✅ Vérification de sécurité
            try:
                self.ecran.blit(self.image_surface, (self.x, self.y))
            except pygame.error:
                pass  # Ignorer les erreurs de blit
        
    def changeImage(self, lien):
        self.lien = lien
        self.creeImage()