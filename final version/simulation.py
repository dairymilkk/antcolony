from bisect import bisect_left
import pygame
import math
from random import randint
import random
import settings as s

s.initialise
s.caption
font = pygame.font.SysFont(None, 30)


def main():
    # class for the colony object
    class colony_class(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.coords = s.colony_position
            self.size = 50
            self.delivered = 0

        def colonyimage(self):
            pygame.draw.circle(s.screen, s.grey, self.coords, self.size)

        def update(self):
            self.colonyimage()

    # class for the food objects
    class food_class(pygame.sprite.Sprite):
        def __init__(self, coord):
            super().__init__()
            self.pos = coord
            self.radius = s.food_radius

        def render(self):
            pygame.draw.circle(s.screen, s.green, self.pos, self.radius)

        def update(self):
            self.render()

    # class for the ant objects

    class ant_class(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.velocity = 1.3
            self.ant_pos = s.colony_position
            self.walking = s.walking_distance
            self.strolling = s.walking_distance
            self.ant_angle = randint(0, 360)
            self.image = pygame.image.load("ant.png").convert_alpha()
            self.himage = pygame.image.load("antfood2.png").convert_alpha()
            self.holding = False
            self.alive = True

        # function for the health of the ant, which decreases every frame
        def health(self):
            if not self.holding:
                self.walking -= 0.03
                self.strolling = s.walking_distance
            if self.holding:
                self.strolling -= 0.03
                self.walking = s.walking_distance
            if self.strolling <= 0:
                self.holding = False

            if self.walking <= 0:
                self.velocity = 0
                self.alive = False
            elif self.walking < 10:
                self.velocity = 0.3
            elif self.walking < 25:
                self.velocity = 0.8
            elif self.walking < 50:
                self.velocity = 1

            if not self.alive and self.walking <= - 1:
                self.kill()

        # function for the random movement of the ant
        def move(self):
            self.ant_angle += self.randangle
            theta = self.ant_angle * (math.pi/180)
            y = math.cos(theta) * self.velocity
            x = math.sin(theta) * self.velocity
            self.ant_pos = (self.ant_pos[0] + x, self.ant_pos[1]+y)

            if self.holding:
                self.rotate = pygame.transform.rotate(
                    self.himage, self.ant_angle)
            else:
                self.rotate = pygame.transform.rotate(
                    self.image, self.ant_angle)
            s.screen.blit(self.rotate, (self.ant_pos),)

        # function for searching for the pheremones, and checking the angle the ant is facing
        def search(self):
            self.p = (self.ant_pos[0] // 10)
            self.z = (self.ant_pos[1] // 10)
            if self.holding:
                if self.ant_angle % 360 >= 315 or self.ant_angle % 360 < 45:
                    self.locate(1, -1, 0, 0)
                elif self.ant_angle % 360 >= 225 and self.ant_angle % 360 < 315:
                    self.locate(0, 0, -1, 1)
                elif self.ant_angle % 360 >= 135 and self.ant_angle % 360 < 225:
                    self.locate(-1, 1, 0, 0)
                elif self.ant_angle % 360 >= 45 and self.ant_angle % 360 < 135:
                    self.locate(0, 0, 1, -1)
            else:
                if self.ant_angle % 360 >= 315 or self.ant_angle % 360 < 45:
                    self.locate2(1, -1, 0, 0)
                elif self.ant_angle % 360 >= 225 and self.ant_angle % 360 < 315:
                    self.locate2(0, 0, -1, 1)
                elif self.ant_angle % 360 >= 135 and self.ant_angle % 360 < 225:
                    self.locate2(-1, 1, 0, 0)
                elif self.ant_angle % 360 >= 45 and self.ant_angle % 360 < 135:
                    self.locate2(0, 0, 1, -1)

        # function for finding the largest blue pheremone
        def locate(self, i, j, k, l):
            if self.holding:
                self.p = ((self.ant_pos[0]) // 10)
                self.z = ((self.ant_pos[1]) // 10)

                self.currenthi = grid[int(self.z) + i][int(self.p) + k]
                self.currenthip = self.p + k
                self.currenthiz = self.z+i
                self.final_rotation = 0

                if grid[int(self.z) + i + k][int(self.p) + j + k] > self.currenthi:
                    self.currenthi = grid[int(
                        self.z)+i + k][int(self.p) + j + k]
                    self.currenthip = self.p + j + k
                    self.currenthiz = self.z + i + k
                    self.final_rotation = -15

                if grid[int(self.z) + i + l][int(self.p) + i + k] > self.currenthi:
                    self.currenthi = grid[int(
                        self.z) + i + l][int(self.p) + i + k]
                    self.currenthip = self.p + i + k
                    self.currenthiz = self.z + i + l
                    self.final_rotation = 15

                if self.currenthi > 10:
                    self.ant_angle += self.final_rotation

                else:
                    self.randangle = randint(-s.rotate, s.rotate)

                if (colony_class().coords[0] - self.ant_pos[0])**2 + (colony_class().coords[1] - self.ant_pos[1])**2 < colony_class().size**2:
                    colony.sprites()[0].delivered += 1
                    self.holding = False

        # function for finding the largest yellow pheremone
        def locate2(self, i, j, k, l):
            if not self.holding:
                self.p = ((self.ant_pos[0]) // 10)
                self.z = ((self.ant_pos[1]) // 10)

                self.currenthi = grid2[int(self.z) + i][int(self.p) + k]
                self.currenthip = self.p + k
                self.currenthiz = self.z+i
                self.final_rotation = 0

                if grid2[int(self.z) + i + k][int(self.p) + j + k] > self.currenthi:
                    self.currenthi = grid2[int(
                        self.z)+i + k][int(self.p) + j + k]
                    self.currenthip = self.p + j + k
                    self.currenthiz = self.z + i + k
                    self.final_rotation = -15

                if grid2[int(self.z) + i + l][int(self.p) + i + k] > self.currenthi:
                    self.currenthi = grid2[int(
                        self.z) + i + l][int(self.p) + i + k]
                    self.currenthip = self.p + i + k
                    self.currenthiz = self.z + i + l
                    self.final_rotation = 15

                if self.currenthi > 10:
                    self.ant_angle += self.final_rotation

                else:
                    self.randangle = randint(-s.rotate, s.rotate)

                # checking if the ant is in contact with some food
                for i in range(0, len(food)):
                    self.foodi = food.sprites()[i].pos
                    # if the ant is in contact with food then it will reduce the size of the food
                    if (self.foodi[0] - self.ant_pos[0])**2 + (self.foodi[1] - self.ant_pos[1])**2 < (food.sprites()[i].radius)**2:
                        food.sprites()[i].radius -= s.nutritionalValue
                        self.dx = (
                            ((colony_class().coords[0])) - self.ant_pos[0])
                        self.dy = (
                            ((colony_class().coords[1])) - self.ant_pos[1])
                        self.tan = 180 * \
                            (math.atan2(self.dx, self.dy))/math.pi
                        self.ant_angle = (self.tan)
                        self.holding = True
                if not self.holding:
                    self.randangle = randint(-s.rotate, s.rotate)

            else:
                self.randangle = randint(-s.rotate, s.rotate)

        # function for the blue pheremone trail, decreases for how long the ant has been walking
        def blue_pheremone(self):
            self.pheremone_counter = 10
            self.p = (self.ant_pos[0] // 10)
            self.z = (self.ant_pos[1] // 10)
            self.strength = math.sqrt((self.ant_pos[0] - colony_class().coords[0])**2 + (
                self.ant_pos[1] - colony_class().coords[1])**2)
            if self.strength != 0:
                grid[int(self.z)][int(self.p)] = 40000/self.strength
                # /self.strength

        # function for the yellow pheremone trail, decrease for how long the ant has been walking with food
        def yellow_pheremone(self):
            self.pheremone_counter += 1
            self.p = (self.ant_pos[0] // 10)
            self.z = (self.ant_pos[1] // 10)
            grid2[int(self.z)][int(self.p)] = 25000/self.pheremone_counter

        # if the ant comes into contact with a wall, it will bounce and also rotate 180 degrees
        def boarder(self):
            if self.ant_pos[0] <= 1:
                self.ant_pos = (self.ant_pos[0] + s.bounce, self.ant_pos[1])
                self.ant_angle -= 180
            if self.ant_pos[1] <= 1:
                self.ant_pos = (self.ant_pos[0], self.ant_pos[1] + s.bounce)
                self.ant_angle -= 180
            if self.ant_pos[0] >= (s.resolution[0] - 12):
                self.ant_pos = (self.ant_pos[0] - s.bounce, self.ant_pos[1])
                self.ant_angle -= 180
            if self.ant_pos[1] >= (s.resolution[1] - 12):
                self.ant_pos = (self.ant_pos[0], self.ant_pos[1] - s.bounce)
                self.ant_angle -= 180

        def update(self):
            self.health()
            self.search()
            if self.holding:
                self.yellow_pheremone()
            else:
                self.blue_pheremone()
            self.move()
            self.boarder()

    # class for population control
    class population_class(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.food_text = font.render(
                (f'Food: {colony.sprites()[0].delivered}'), True, s.white)
            self.ant_text = font.render(
                (f'Ants: {s.ant_num}'), True, s.white)
            self.threshold = s.breeding_threshold

        # function for the reproduction method
        def reproduce(self):
            if colony.sprites()[0].delivered % s.breeding_frequency == 0 and colony.sprites()[0].delivered >= self.threshold:
                ants.add(ant_class())
                self.threshold += s.breeding_frequency

        # function for the displaying of number and ants and amount of food that has been collected
        def display(self):
            self.food_text = font.render(
                (f'Food: {colony.sprites()[0].delivered}'), True, s.white)
            self.ant_text = font.render(
                (f'Ants: {len(ants)}'), True, s.white)
            s.screen.blit(self.food_text, (25, 20))
            s.screen.blit(self.ant_text, (25, 40))

        def update(self):
            self.reproduce()
            self.display()

    # generate food function
    def generate_food():
        positions = []
        randompos = (randint(0, s.resolution[0]), randint(0, s.resolution[1]))
        num = 0
        while num < s.food_num:
            passed = 0
            if (randompos[0] - s.centre[0])**2 + (randompos[1] - s.centre[1])**2 > s.distanceFromColony:
                if num == 0:
                    positions.append(randompos)
                    num += 1
                    randompos = (randint(0, s.resolution[0]), randint(
                        0, s.resolution[1]))
                else:
                    passed = 0
                    for i in range(len(positions)):
                        newpos = positions[i]
                        if (randompos[0] - newpos[0])**2 + (randompos[1] - newpos[1])**2 > s.distanceFromEachOther:
                            passed += 1
                    if passed == len(positions):
                        positions.append(randompos)
                        num += 1
                        randompos = (randint(0, s.resolution[0]), randint(
                            0, s.resolution[1]))
                    else:
                        randompos = (randint(0, s.resolution[0]), randint(
                            0, s.resolution[1]))
            else:
                randompos = (randint(0, s.resolution[0]), randint(
                    0, s.resolution[1]))
        for i in range(0, s.food_num):
            food.add(food_class(positions[i]))

    food = pygame.sprite.Group()
    generate_food()

    ants = pygame.sprite.Group()
    for i in range(0, s.ant_num):
        ants.add(ant_class())

    colony = pygame.sprite.Group()
    colony.add(colony_class())
    active = True

    population_control = pygame.sprite.Group()
    population_control.add(population_class())

    # creation of the grid
    rows, cols = [s.resolution[1] // 10, s.resolution[0] // 10]
    grid = [[0 for i in range(cols)] for j in range(rows)]
    grid2 = [[0 for i in range(cols)] for j in range(rows)]

    # deletes food when it has all been eaten
    def food_delete():
        if len(food) > 0:
            for i in range(len(food)):
                if food.sprites()[i-1].radius < 1:
                    food.remove(food.sprites()[i-1])

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False

        s.screen.fill(s.black)

        # drawing the pheremones on the screen
        for i in range(len(grid)-1):
            for j in range(len(grid[i])-1):
                if grid[i][j] > 255 and grid2[i][j] > 255:
                    pygame.draw.circle(s.screen, (255, 255, 255), (((
                        j * 10)+10), ((i * 10)+10)), (1))
                elif grid[i][j] > 255 and grid2[i][j] >= 0:
                    pygame.draw.circle(s.screen, (grid2[i][j], grid2[i][j], 255), (((
                        j * 10)+10), ((i * 10)+10)), (1))
                elif grid2[i][j] > 255 and grid[i][j] >= 0:
                    pygame.draw.circle(s.screen, (255, 255, grid[i][j]), (((
                        j * 10)+10), ((i * 10)+10)), (1))
                elif grid[i][j] > 1 or grid2[i][j] > 1:
                    pygame.draw.circle(s.screen, (grid2[i][j], grid2[i][j], grid[i][j]), (((
                        j * 10)+10), ((i * 10)+10)), (1))

                # pheremone diffusion
                if grid[i][j] > 1:
                    grid[i][j] -= s.pheremone_length
                if grid2[i][j] > 1:
                    grid2[i][j] -= s.pheremone_length

        # if theres no food then generate new food
        if len(food) <= 0:
            generate_food()

        food_delete()
        food.update()
        ants.update()
        colony.update()
        population_control.update()

        pygame.display.update()
        s.clock.tick(60)
