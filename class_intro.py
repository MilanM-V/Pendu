import pygame
import math
import random



class Particule:
    def __init__(self,x,y,couleur,fond=False,width=1920,height=1080):
        self.x=x
        self.y=y
        self.fond = fond
        self.couleur = couleur
        self.width=width
        self.height=height
        if self.fond:
            self.vitesse_x=random.uniform(-0.5,0.5)
            self.vitesse_y=random.uniform(-0.5,0.5)
            self.taille=random.randint(2,4)
            self.duree=255
            self.pv=0
        else:
            self.vitesse_x=random.uniform(-4,4)
            self.vitesse_y=random.uniform(-6,-2)
            self.taille=random.randint(3,6)
            self.duree=255
            self.pv=8

    def update(self):
        self.x+=self.vitesse_x
        self.y+=self.vitesse_y
        if not self.fond:
            self.vitesse_y+=0.2
            self.taille-=0.1
            self.duree-=self.pv
        else:
            if self.x<0 or self.x>self.width: 
                self.vitesse_x*=-1
            if self.y<0 or self.y>self.height: 
                self.vitesse_y*=-1

    def dessiner(self,surface):
        if self.duree>0 and self.taille>0:
            ecran=pygame.Surface((int(self.taille*2),int(self.taille*2)),pygame.SRCALPHA)
            alpha=int(self.duree)
            pygame.draw.circle(ecran,(*self.couleur,alpha),(int(self.taille),int(self.taille)),int(self.taille))
            surface.blit(ecran,(self.x-self.taille,self.y-self.taille))

class Lettre:
    def __init__(self,charactere,font,couleur,final_x,final_y,delay_frames):
        self.charactere=charactere
        self.font=font
        self.couleur=couleur
        self.image=font.render(charactere,True,couleur)
        self.ombre=font.render(charactere,True,(0,100,100)) 
        self.x=final_x
        self.final_y=final_y
        self.start_y=-150
        self.y=self.start_y
        self.vitesse_y=0
        self.gravity=0.6
        self.rebon=-0.5
        self.drop=False
        self.dropGo=False 
        self.delay_frames=delay_frames
        self.timer=0
        self.active=False

    def update(self):
        self.dropGo=False 
        if not self.active:
            self.timer+=1
            if self.timer>=self.delay_frames:
                self.active=True
            return
        if not self.drop:
            self.vitesse_y+=self.gravity
            self.y+=self.vitesse_y
            if self.y>=self.final_y:
                self.y=self.final_y
                if abs(self.vitesse_y)>2:
                    self.dropGo=True 
                self.vitesse_y*=self.rebon
                if abs(self.vitesse_y)<1:
                    self.vitesse_y=0
                    self.drop=True

    def dessiner(self,surface):
        if self.active:
            surface.blit(self.ombre,(self.x+2,self.y+2))
            surface.blit(self.image,(self.x,self.y))


class IntroScene:
    def __init__(self,width,height,text):
        self.width=width
        self.height=height
        self.font=pygame.font.SysFont("comicsansms", int(80*height/1080), bold=True)
        self.couleur=(6,182,212)
        self.base_y=height//2.5

        self.particles=[]
        for i in range(120):
            self.particles.append(Particule(random.randint(0,width),random.randint(0,height),(30,50,80),fond=True,width=width,height=height))

        self.act="texteIntro"
        self.intro_timer=0
        self.intro_font=pygame.font.SysFont("couriernew", int(60*height/1080))
        self.intro_scale=1.0

        self.letters=[]
        total_width=sum(self.font.size(c)[0] for c in text)
        x=(width-total_width)//2

        for i,charactere in enumerate(text):
            widthNow=self.font.size(charactere)[0]
            self.letters.append(Lettre(charactere,self.font,self.couleur,x,self.base_y,i*6))
            x+=widthNow

        self.full_text=pygame.Surface((total_width+20,150),pygame.SRCALPHA)
        xAct=10
        for charactere in text:
            img=self.font.render(charactere,True,self.couleur)
            glow=self.font.render(charactere,True,(0,100,200))
            self.full_text.blit(glow,(xAct-2,2)) 
            self.full_text.blit(img,(xAct,0))
            xAct+=img.get_width()

        self.rotationTime=0
        self.rotationX=width//2
        self.rotationY=-100
        self.penduLongueur=self.base_y-self.rotationY+60
        self.fini=False
        
    def actualiser_dimensions(self,width,height,text):
        self.width=width
        self.height=height
        self.font=pygame.font.SysFont("comicsansms", int(80*height/1080), bold=True)
        self.couleur=(6,182,212)
        self.base_y=height//2.5

        self.particles=[]
        for i in range(120):
            self.particles.append(Particule(random.randint(0,width),random.randint(0,height),(30,50,80),fond=True,width=width,height=height))

        self.act="texteIntro"
        self.intro_timer=0
        self.intro_font=pygame.font.SysFont("couriernew", int(60*height/1080))
        self.intro_scale=1.0

        self.letters=[]
        total_width=sum(self.font.size(c)[0] for c in text)
        x=(width-total_width)//2

        for i,charactere in enumerate(text):
            widthNow=self.font.size(charactere)[0]
            self.letters.append(Lettre(charactere,self.font,self.couleur,x,self.base_y,i*6))
            x+=widthNow

        self.full_text=pygame.Surface((total_width+20,150),pygame.SRCALPHA)
        xAct=10
        for charactere in text:
            img=self.font.render(charactere,True,self.couleur)
            glow=self.font.render(charactere,True,(0,100,200))
            self.full_text.blit(glow,(xAct-2,2)) 
            self.full_text.blit(img,(xAct,0))
            xAct+=img.get_width()

        self.rotationTime=0
        self.rotationX=width//2
        self.rotationY=-100
        self.penduLongueur=self.base_y-self.rotationY+60
        self.fini=False
    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.duree<=0:
                self.particles.remove(p)
        if self.act=="texteIntro":
            self.intro_timer+=1
            self.intro_scale=1.0+math.sin(self.intro_timer*0.05)*0.05
            if self.intro_timer>150:
                self.act="drop"

        elif self.act=="drop":
            allDrop=True
            for letter in self.letters:
                letter.update()
                if letter.dropGo:
                    for i in range(10):
                        self.particles.append(Particule(letter.x+ 20,letter.y+80,(255,255,255),width=self.width,height=self.height,fond=False))
                if not letter.drop:
                    allDrop=False
            if allDrop:
                self.act="balance"
        elif self.act=="balance":
            self.rotationTime+=0.05

    def gestionBalance(self,event):
        if self.act=="balance":
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                self.fini=True

    def draw(self, screen):
        screen.fill((15,23,42))
        for p in self.particles:
            p.dessiner(screen)
        if self.act == "texteIntro":
            alpha=255
            if self.intro_timer<30: 
                alpha=int(self.intro_timer*255/30)
            if self.intro_timer>120:
                alpha=int(255-(self.intro_timer-120)*8.5)
            if alpha<0: 
                alpha=0
            titre=self.intro_font.render("PROJET BY MILAN",True,(255,255,255))
            w=int(titre.get_width()*self.intro_scale)
            h=int(titre.get_height()*self.intro_scale)
            scaled_txt=pygame.transform.scale(titre,(w,h))
            scaled_txt.set_alpha(alpha)
            rect=scaled_txt.get_rect(center=(self.width//2,self.height//2))
            screen.blit(scaled_txt, rect)
        elif self.act=="drop":
            for letter in self.letters:
                letter.dessiner(screen)
        elif self.act=="balance":
            angle=math.sin(self.rotationTime) * 0.2
            deg=math.degrees(angle)
            xAct=self.rotationX-self.penduLongueur*math.sin(angle)
            yAct=self.rotationY+self.penduLongueur*math.cos(angle)
            img=pygame.transform.rotate(self.full_text,deg)
            rect=img.get_rect(center=(xAct,yAct))
            corde_endX=self.rotationX-(self.penduLongueur-50)*math.sin(angle)
            corde_endY=self.rotationY+(self.penduLongueur-50)*math.cos(angle)
            pygame.draw.line(screen,(150,150,150),(self.rotationX,0),(corde_endX,corde_endY),3)
            screen.blit(img,rect)
            if int(self.rotationTime*3)%2==0:
                font=pygame.font.SysFont("arial",int(20*self.height/1080))
                msg=font.render("Appuyez sur ESPACE",True,(100,200,200))
                screen.blit(msg,(self.width//2-msg.get_width()//2,self.height-80))

