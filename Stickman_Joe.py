import pygame
import sys
import random


class Button:
    def __init__(self, surface, color, x, y, width, height, text=''):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = True

    def draw(self, outline=None):
        if outline:
            pygame.draw.rect(self.surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(self.surface, self.color if self.active else (100, 100, 100),
                         (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont(None, 30)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            self.surface.blit(text_surface, text_rect)

    def is_over(self, pos):
        if self.active:  # Check if the button is active
            if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
                return True
        return False


class Key:
    def __init__(self, surface, image_path, x, y):
        self.surface = surface
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image if necessary
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw_key(self):
        if not self.clicked:  # Only draw if the key hasn't been clicked
            self.surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        if not self.clicked and self.rect.collidepoint(pos):  # Check if the key hasn't been clicked and is clicked now
            self.clicked = True
            return True
        return False


class SkærmTæller:
    def __init__(self):
        pygame.init()
        self.skaerm_bredde = 800
        self.skaerm_hoejde = 600
        self.skaerm = pygame.display.set_mode((self.skaerm_bredde, self.skaerm_hoejde))
        pygame.display.set_caption("Skærmtæller")
        self.font = pygame.font.SysFont(None, 30)
        self.koerer = True
        self.nuvaerende_skaerm = 0
        self.skaerm_stack = []
        self.start_button = Button(self.skaerm, (0, 0, 0), 400, 275, 200, 50, "Start")
        self.left_button = Button(self.skaerm, (0, 0, 0), 50, 200, 50, 200, "Venstre")
        self.right_button = Button(self.skaerm, (0, 0, 0), 700, 200, 50, 200, "Højre")
        self.key1 = Key(self.skaerm, "KEy_2.png", 100, 100)  # First key
        self.key2 = Key(self.skaerm, "KEy_1.png", 600, 100)  # Second key
        self.key3 = Key(self.skaerm, "KEy_2.png", 300, 100)  # Third key
        self.key1_clicked = False
        self.key2_clicked = False
        self.key3_clicked = False
        self.screen_4_button = Button(self.skaerm, (255, 0, 255), 300, 300, 50, 50, "Æg")
        self.screen_5_button = Button(self.skaerm, (255, 0, 255), 300, 200, 50, 50, "Æble")
        self.screen_6_button = Button(self.skaerm, (255, 0, 255), 300, 100, 50, 50, "Mælk")
        self.screen_9_button = Button(self.skaerm, (255, 0, 255), 400, 200, 50, 50, "Banan")
        self.screen_10_button = Button(self.skaerm, (255, 0, 255), 400, 300, 50, 50, "Sten")
        self.screen_11_button = Button(self.skaerm, (255, 0, 255), 300, 400, 50, 50, "Gren")
        self.screen_12_button = Button(self.skaerm, (255, 0, 255), 400, 100, 50, 50, "Stol")
        self.screen_13_button = Button(self.skaerm, (255, 0, 255), 400, 400, 50, 50, "Cement")
        self.buttons_clicked = {self.screen_4_button: False,
                                self.screen_5_button: False,
                                self.screen_6_button: False,
                                self.screen_9_button: False}
        self.right_button_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.koerer = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if len(self.skaerm_stack) > 0:
                        self.nuvaerende_skaerm = self.skaerm_stack.pop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.nuvaerende_skaerm == 0:
                    if event.button == pygame.BUTTON_LEFT and self.start_button.is_over(event.pos):
                        self.nuvaerende_skaerm = 1
                elif self.nuvaerende_skaerm >= 1:
                    if event.button == pygame.BUTTON_LEFT and self.right_button.is_over(event.pos):
                        self.nuvaerende_skaerm += 1
                        self.skaerm_stack.append(self.nuvaerende_skaerm - 1)
                        if self.nuvaerende_skaerm == 2:
                            self.skaerm.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                            self.key1_clicked = False  # Reset key1 click flag when transitioning to screen 2
                        elif self.nuvaerende_skaerm == 3:
                            self.skaerm.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                            self.key2_clicked = False  # Reset key2 click flag when transitioning to screen 3
                        elif self.nuvaerende_skaerm == 4:
                            self.skaerm.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                            self.key3_clicked = False  # Reset key3 click flag when transitioning to screen 4
                            # Reset buttons clicked state for screen 4 buttons
                            for button in self.buttons_clicked:
                                self.buttons_clicked[button] = False
                        elif self.nuvaerende_skaerm == 6:
                            self.right_button_active = False  # Deactivate the "Højre" button on screen 6
                    elif event.button == pygame.BUTTON_LEFT and self.left_button.is_over(event.pos):
                        if self.nuvaerende_skaerm != 1:  # Make left button unclickable if not on screen 1
                            self.nuvaerende_skaerm -= 1
                    elif event.button == pygame.BUTTON_LEFT and self.key1.is_clicked(event.pos):
                        self.key1_clicked = True
                        print("The first key has been clicked")
                    elif event.button == pygame.BUTTON_LEFT and self.key2.is_clicked(event.pos):
                        self.key2_clicked = True
                        print("The second key has been clicked")
                    elif event.button == pygame.BUTTON_LEFT and self.key3.is_clicked(event.pos):
                        self.key3_clicked = True
                        print("The third key has been clicked")
                    elif (event.button == pygame.BUTTON_LEFT and
                          self.nuvaerende_skaerm == 4 and
                          (self.screen_4_button.is_over(event.pos) or
                           self.screen_5_button.is_over(event.pos) or
                           self.screen_6_button.is_over(event.pos) or
                           self.screen_9_button.is_over(event.pos))):
                        for button in self.buttons_clicked:
                            if button.is_over(event.pos):
                                self.buttons_clicked[button] = True
                        if all(self.buttons_clicked.values()):
                            print("All buttons on screen 4 have been clicked")
                            self.right_button_active = True

    def draw_screen(self):
        if self.nuvaerende_skaerm == 0:
            background_img = pygame.image.load("Startskrm_eksamensprojekt.png")
            background_img = pygame.transform.scale(background_img, (self.skaerm_bredde, self.skaerm_hoejde))

            self.skaerm.blit(background_img, (0, 0))

            self.start_button.active = True
            self.start_button.draw()
        elif self.nuvaerende_skaerm >= 1 and self.nuvaerende_skaerm < 4:
            if self.nuvaerende_skaerm == 1:
                self.skaerm.fill((255, 255, 255))
                if not self.key1_clicked:
                    self.key1.draw_key()
            elif self.nuvaerende_skaerm == 2:
                self.skaerm.fill((255, 0, 0))
                if not self.key2_clicked:
                    self.key2.draw_key()
            elif self.nuvaerende_skaerm == 3:
                self.skaerm.fill((0, 255, 0))
                if not self.key3_clicked:
                    self.key3.draw_key()

            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))

            # Only draw the left button if not on screen 1
            if self.nuvaerende_skaerm != 1:
                self.left_button.active = True
                self.left_button.color = (0, 0, 0)  # Update the color to make it visible
                self.left_button.draw()

            # Check if the corresponding key is clicked to activate the right button
            if self.nuvaerende_skaerm == 1 and self.key1.clicked:
                self.right_button.active = True
                self.right_button.draw()
            elif self.nuvaerende_skaerm == 2 and self.key2.clicked:
                self.right_button.active = True
                self.right_button.draw()
            elif self.nuvaerende_skaerm == 3 and self.key3.clicked:
                self.right_button.active = True
                self.right_button.draw()
            else:
                self.right_button.active = False

        elif self.nuvaerende_skaerm == 4:
            self.skaerm.fill((0, 0, 255))
            # Draw the "Venstre" button on screen 4
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()

            # Draw screen 4 buttons
            self.screen_4_button.draw()
            self.screen_5_button.draw()
            self.screen_6_button.draw()
            self.screen_9_button.draw()
            self.screen_10_button.draw()
            self.screen_11_button.draw()
            self.screen_12_button.draw()
            self.screen_13_button.draw()

            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))

            # Draw the "Højre" button only if all buttons on screen 4 have been clicked
            if self.right_button_active:
                self.right_button.active = True
                self.right_button.color = (0, 0, 0)  # Set the color of "Højre" button to black
                self.right_button.draw()
        elif self.nuvaerende_skaerm == 5:
            self.skaerm.fill((255, 255, 0))
            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            # Draw the "Venstre" button on screen 5
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()
            # Draw the "Højre" button on screen 5
            self.right_button.active = True
            self.right_button.color = (0, 0, 0)
            self.right_button.draw()
        elif self.nuvaerende_skaerm == 6:
            self.skaerm.fill((255, 0, 255))
            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            # Draw the "Venstre" button on screen 6
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()
            # Draw the "Højre" button on screen 6
            self.right_button.active = True
            self.right_button.color = (0, 0, 0)
            self.right_button.draw()

        elif self.nuvaerende_skaerm == 7:
            self.skaerm.fill((0, 255, 255))
            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            # Draw the "Venstre" button on screen 7
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()
            # Draw the "Højre" button on screen 7
            self.right_button.active = True
            self.right_button.color = (0, 0, 0)
            self.right_button.draw()

        elif self.nuvaerende_skaerm == 8:
            self.skaerm.fill((0, 255, 255))
            # Draw screen number
            skaermtal_tekst = self.font.render(f"Skærm {self.nuvaerende_skaerm}", True, (0, 0, 0))
            self.skaerm.blit(skaermtal_tekst, (self.skaerm_bredde // 2 - skaermtal_tekst.get_width() // 2, 20))
            # Draw the "Venstre" button on screen 8
            self.left_button.active = True
            self.left_button.color = (0, 0, 0)
            self.left_button.draw()

        pygame.display.flip()

    def koer_spil(self):
        while self.koerer:
            self.handle_events()
            self.draw_screen()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    spil = SkærmTæller()
    spil.koer_spil()