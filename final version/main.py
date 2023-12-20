import simulation
import settings as s
import pygame
import settingspage
from random import randint
import math

s.initialise
s.caption
active = True
font = pygame.font.SysFont(None, 50)

# function for displaying the title of the menu


def title():
    title_text = font.render(f'Ant Colony Sim', True, s.red)
    s.screen.blit(title_text, (s.centre[0] - 130, s.centre[1] - 100))

# function for the run button


def run_button():
    play_button = pygame.draw.rect(
        s.screen, s.red, (s. centre[0] - 100, s.centre[1] - 20, 200, 70), 0, 5)
    play_text = font.render(f'RUN', True, s.black)
    # checks if the mouse is touching the button
    if play_button.collidepoint(pygame.mouse.get_pos()):
        play_button = pygame.draw.rect(
            s.screen, s.black, (s.centre[0] - 100, s.centre[1] - 20, 200, 70))
        play_text = font.render(f'RUN', True, s.red)
        # checks if the mouse is clicked
        if pygame.mouse.get_pressed()[0] == 1:
            simulation.main()
    s.screen.blit(play_text, (s.centre[0] - 40, s.centre[1]))

# function for the settings button


def settings_button():
    settings_button = pygame.draw.rect(
        s.screen, s.red, (s.centre[0] - 100, s.centre[1] + 80, 200, 70), 0, 5)
    settings_text = font.render(f'SETTINGS', True, s.black)
    # checks if the mouse is touching the button
    if settings_button.collidepoint(pygame.mouse.get_pos()):
        settings_button = pygame.draw.rect(
            s.screen, s.black, (s.centre[0] - 100, s.centre[1] + 80, 200, 70))
        settings_text = font.render(f'SETTINGS', True, s.red)
        # checks if the mouse is clicked
        if pygame.mouse.get_pressed()[0] == 1:
            settingspage.main()
    s.screen.blit(settings_text, (s.centre[0]-85, s.centre[1] + 100))

# ant class


class ant_class(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocity = 1
        self.ant_pos = (
            randint(0, s.resolution[0]), randint(0, s.resolution[1]))
        self.maxvel = 3
        self.minvel = 0
        self.ant_angle = randint(0, 360)
        self.direction = 0
        self.randangle = 0
        self.image = pygame.image.load("ant.png").convert_alpha()

    # function for the movement of the ant
    def move(self):
        self.randangle += randint(-200, 200)*0.01
        self.direction += self.randangle
        if self.direction >= 2 or self.direction <= -2:
            self.direction -= self.randangle
        randacc = randint(-75, 75)*0.01
        self.velocity += randacc
        if self.velocity >= self.maxvel or self.velocity <= self.minvel:
            self.velocity -= randacc
        self.ant_angle += self.direction
        theta = self.ant_angle * (math.pi/180)
        y = math.cos(theta) * self.velocity
        x = math.sin(theta) * self.velocity
        self.ant_pos = (self.ant_pos[0] + x, self.ant_pos[1]+y)
        self.rotate = pygame.transform.rotate(
            self.image, self.ant_angle)
        s.screen.blit(self.rotate, (self.ant_pos),)

    def update(self):
        self.move()


ant = pygame.sprite.Group()
for i in range(0, 100):
    ant.add(ant_class())

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False

    s.screen.fill((0, 0, 0))

    title()
    run_button()
    settings_button()
    ant.update()

    pygame.display.update()
    s.clock.tick(60)
