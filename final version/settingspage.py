import simulation
import settings as s
import pygame
import pygame_textinput
import settingspage
from random import randint
import math

s.initialise
s.caption


def main():
    font = pygame.font.SysFont(None, 50)
    small_font = pygame.font.SysFont(None, 30)

    # function to centre the text to the text box

    def centre(length):
        position = 45 - (length * 5)
        return position

    # function for the title

    def ant_num(value):
        s.ant_num = int(value)
        return s.ant_num

    def food_num(value):
        if value > 10:
            value = 10
        s.food_num = int(value)
        return s.food_num

    def pheremone_length(value):
        if value > 1:
            value = 1
        s.pheremone_length = value
        return s.pheremone_length

    def breeding_threshold(value):
        s.breeding_threshold = int(value)
        return s.breeding_threshold

    def breeding_frequency(value):
        if value < 1:
            value = 1
        s.breeding_frequency = int(value)
        return s.breeding_frequency

    def walking_distance(value):
        s.walking_distance = int(value)
        return s.walking_distance

    def title():
        title_text = font.render(f'Settings', True, s.red)
        s.screen.blit(title_text, (s.centre[0] - 75, s.centre[1] - 200))

    class button_class(pygame.sprite.Sprite):
        def __init__(self, rectx, recty, text, variable, textx, texty, inputx, inputy, method):
            super().__init__()
            self.textinput = pygame_textinput.TextInputVisualizer(
                font_object=small_font)
            self.clicked = False
            self.rectx = rectx
            self.recty = recty
            self.text = text
            self.variable = variable
            self.textx = textx
            self.texty = texty
            self.inputx = inputx
            self.method = method
            self.inputy = inputy

        def main(self):
            button = pygame.draw.rect(
                s.screen, s.red, (s. centre[0] - self.rectx, s.centre[1] - self.recty, 90, 35), 0, 5)
            self.textinput.update(events)

            text = small_font.render(f'{self.text}', True, s.red)
            num = small_font.render(f'{self.variable}', True, s.black)

            s.screen.blit(
                text, (s.centre[0] - self.textx, s.centre[1] - self.texty))
            if self.clicked:
                if len(self.textinput.value) > 4:
                    self.textinput.value = self.textinput.value[1:]
                s.screen.blit(
                    self.textinput.surface, (s.centre[0] - self.inputx + centre(len(self.textinput.value)), s.centre[1] - self.inputy))

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN or (pygame.mouse.get_pressed()[0] == 1 and not button.collidepoint(pygame.mouse.get_pos())):
                    try:
                        if int(self.textinput.value)< 0:
                            self.textinput.value *= -1
                        self.method(int(self.textinput.value))
                        self.variable = self.method(int(self.textinput.value))

                    except:
                        try:
                            if float(self.textinput.value)< 0:
                                self.textinput.value *= -1
                            self.method(float(self.textinput.value))
                            self.variable = self.method(
                                float(self.textinput.value))
                        except:
                            self.variable = self.variable
                    self.clicked = False
            else:
                if button.collidepoint(pygame.mouse.get_pos()):
                    num = small_font.render(f'{self.variable}', True, s.white)
                    if pygame.mouse.get_pressed()[0] == 1:
                        self.textinput.value = ""
                        self.clicked = True
                    else:
                        s.screen.blit(
                            num, (s.centre[0] - self.inputx + centre(len(str(self.variable))), s.centre[1] - self.inputy))
                else:
                    s.screen.blit(
                        num, (s.centre[0] - self.inputx + centre(len(str(self.variable))), s.centre[1] - self.inputy))

        def update(self):
            self.main()

    # class for the ants

    class ant_class(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.velocity = 1
            self.ant_pos = randint(
                0, s.resolution[0]), randint(0, s.resolution[1])
            self.maxvel = 3
            self.minvel = 0
            self.ant_angle = randint(0, 360)
            self.direction = 0
            self.randangle = 0
            self.image = pygame.image.load("ant.png").convert_alpha()

        # function for the movement of the ants
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

    active = True

    ant = pygame.sprite.Group()
    for i in range(0, 100):
        ant.add(ant_class())

    button_group = pygame.sprite.Group()
    button_group.add(button_class(250, 80, "Number Of Ants",
                                  s.ant_num, 280, 105, 250, 72, ant_num))
    button_group.add(button_class(50, 80, "Number Of Food",
                                  s.food_num, 80, 105, 50, 72, food_num))
    button_group.add(button_class(-150, 80, "Pheremone Diffusion",
                                  s.pheremone_length, -100, 105, -150, 72, pheremone_length))
    button_group.add(button_class(-150, -20, "Breeding Threshold",
                                  s.breeding_threshold, -115, 5, -150, -28, breeding_threshold))
    button_group.add(button_class(50, -20, "Breeding Frequency",
                                  s.breeding_frequency, 95, 5, 50, -28, breeding_frequency))
    button_group.add(button_class(250, -20, "Walking Distance",
                                  s.walking_distance, 280, 5, 250, -28, walking_distance))

    while active:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                active = False

        s.screen.fill((s.black))
        title()
        button_group.update()

        ant.update()

        pygame.display.update()
        s.clock.tick(60)
