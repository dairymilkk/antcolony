# libraries
import pygame

# size of the screen
resolution = (700, 700)
# centre of the screen
centre = (resolution[0]/2, resolution[1]/2)

# colours
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
grey = (125, 125, 125)
yellow = (255, 255, 0)

# initialisation
initialise = pygame.init()
caption = pygame.display.set_caption("ants")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((resolution))

# simulation settings
# colony settings
colony_position = (centre[0], centre[1])
# food settings
food_num = 5
food_radius = 50
nutritionalValue = 0.07
# ant settings
bounce = 100
ant_num = 250
rotate = 15
breeding_threshold = 100
breeding_frequency = 25
walking_distance = 100

# phermone settings
pheremone_length = .1


# generation_code
distanceFromColony = 50000
distanceFromEachOther = 30000
