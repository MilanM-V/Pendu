import pygame


class Fenetre:
    def __init__(self,x,y,titre,couleurFond=(250,250,250)):
        self.largeurBase=x
        self.hauteurBase=y
        self.largeurAct=x
        self.hauteurAct=y
        self.titre=titre
        self.fullscreenInfo=False
        self.couleurFond=couleurFond
    def creer_fenetre(self):
        #methode pour creer la fenetre
        self.fenetre=pygame.display.set_mode((self.largeurBase, self.hauteurBase))
        pygame.display.set_caption(self.titre)
        
        return self.fenetre
    def fullscreen(self):
        #methode pour mettre la fenetre en fullscreen
        if not self.fullscreenInfo:
            self.fenetre=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreenInfo=True
            info=pygame.display.Info()
            self.largeurAct=info.current_w
            self.hauteurAct=info.current_h
        else:
            self.fenetre=pygame.display.set_mode((self.largeurBase, self.hauteurBase))
            self.fullscreenInfo=False
            self.largeurAct=self.largeurBase
            self.hauteurAct=self.hauteurBase
        pygame.display.flip()
        return self.fenetre
    def dessiner(self):
        self.fenetre.fill(self.couleurFond)

    





