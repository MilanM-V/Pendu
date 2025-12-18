import pygame
import math

class DroppingLetter:
    """Gère une lettre individuelle qui tombe."""
    def __init__(self, char, font, color, final_x, final_y, delay):
        self.image = font.render(char, True, color)
        self.x = final_x
        self.final_y = final_y
        self.y = -100 - (delay * 150) # Départ hors écran
        self.vy = 0
        self.gravity = 0.8
        self.bounce = -0.5
        self.landed = False

    def update(self):
        if not self.landed:
            self.vy += self.gravity
            self.y += self.vy
            
            # Contact avec le sol
            if self.y >= self.final_y:
                self.y = self.final_y
                self.vy *= self.bounce
                # Arrêt si le rebond est trop faible
                if abs(self.vy) < 1:
                    self.vy = 0
                    self.landed = True

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class IntroScene:
    """Gère toute la scène d'intro (Chute + Balancier)."""
    def __init__(self, screen_width, screen_height, text="LE PENDU"):
        self.width = screen_width
        self.height = screen_height
        
        # --- Configuration ---
        self.font = pygame.font.SysFont("comicsansms", 80)
        self.color = (255, 215, 0) # Or
        self.rope_color = (120, 120, 120)
        
        # --- Calculs de positionnement ---
        self.base_y = screen_height // 3  # Hauteur d'atterrissage
        
        # 1. Création des lettres individuelles
        self.letters = []
        total_width = 0
        spacings = []
        
        # Pré-calcul de la largeur pour centrer
        for char in text:
            w = self.font.size(char)[0]
            spacings.append(w)
            total_width += w
            
        current_x = (self.width - total_width) // 2
        
        for i, char in enumerate(text):
            # i * 4 crée le décalage de chute entre les lettres
            self.letters.append(DroppingLetter(char, self.font, self.color, current_x, self.base_y, i * 4))
            current_x += spacings[i]

        # 2. Création de la surface fusionnée (pour le balancier)
        self.full_text_surf = pygame.Surface((total_width, 150), pygame.SRCALPHA)
        cx = 0
        for i, char in enumerate(text):
            char_img = self.font.render(char, True, self.color)
            self.full_text_surf.blit(char_img, (cx, 0))
            cx += spacings[i]

        # --- Variables d'état ---
        self.state = "DROPPING" # ou "SWINGING"
        self.is_finished = False # Devient True quand le joueur appuie sur ESPACE
        
        # --- Physique du pendule ---
        self.swing_time = 0
        self.pivot_x = self.width // 2
        self.pivot_y = -100
        # Calcul précis de la longueur de corde pour éviter le saut
        self.rope_length = self.base_y - self.pivot_y + (self.full_text_surf.get_height() // 2)

    def update(self):
        """Met à jour la logique. À appeler à chaque frame."""
        
        if self.state == "DROPPING":
            all_landed = True
            for letter in self.letters:
                letter.update()
                if not letter.landed:
                    all_landed = False
            
            if all_landed:
                # Transition automatique
                self.state = "SWINGING"

        elif self.state == "SWINGING":
            self.swing_time += 0.05

    def handle_event(self, event):
        """Gère les entrées clavier pour cette scène."""
        if self.state == "SWINGING" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.is_finished = True # Signal pour le main.py de changer d'écran

    def draw(self, screen):
        """Dessine l'état actuel sur l'écran."""
        
        if self.state == "DROPPING":
            for letter in self.letters:
                letter.draw(screen)

        elif self.state == "SWINGING":
            # Calcul de l'angle
            angle_rad = math.sin(self.swing_time) * 0.15
            angle_deg = math.degrees(angle_rad)

            # Calcul position du texte
            text_center_x = self.pivot_x - (self.rope_length * math.sin(angle_rad))
            text_center_y = self.pivot_y + (self.rope_length * math.cos(angle_rad))

            # Rotation de l'image
            rotated_img = pygame.transform.rotate(self.full_text_surf, angle_deg)
            new_rect = rotated_img.get_rect(center=(text_center_x, text_center_y))

            # Corde
            rope_end_x = self.pivot_x - ((self.rope_length - 40) * math.sin(angle_rad))
            rope_end_y = self.pivot_y + ((self.rope_length - 40) * math.cos(angle_rad))
            pygame.draw.line(screen, self.rope_color, (self.pivot_x, 0), (rope_end_x, rope_end_y), 4)

            # Texte
            screen.blit(rotated_img, new_rect)
            
            # Message clignotant
            if int(self.swing_time * 2) % 2 == 0:
                font_msg = pygame.font.SysFont("arial", 20)
                msg = font_msg.render("Appuyez sur ESPACE", True, (150, 150, 150))
                screen.blit(msg, (self.width//2 - msg.get_width()//2, self.height - 50))
                
import pygame
# from intro import IntroScene  <-- Si tu as mis la classe dans un fichier intro.py

# Setup basique
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 1. On instancie l'animation
intro = IntroScene(WIDTH, HEIGHT, text="LE PENDU")

# --- BOUCLE DE L'INTRO ---
intro_running = True
while intro_running:
    screen.fill((20, 20, 30)) # Fond sombre
    
    # Gestion des événements via la classe
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            intro_running = False
            pygame.quit()
            exit()
            
        # On passe l'événement à la classe Intro
        intro.handle_event(event)

    # Si l'intro signale qu'elle est finie (Space appuyé), on sort de la boucle
    if intro.is_finished:
        intro_running = False

    # Mise à jour et Dessin
    intro.update()
    intro.draw(screen)

    pygame.display.flip()
    clock.tick(60)

# --- LE VRAI JEU COMMENCE ICI ---
print("Lancement du jeu principal...")
# while game_running: ...