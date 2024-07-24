import pygame
import random
import os

number_of_cars = 1
screen_width   = 800
screen_height  = 600

# place Pygame window at a specific location
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)

# Classes
class Vehicle:
    def __init__(self, colour = "red", x = 400, y = 400):
        self.img_path = "vehicles/" + colour + ".png"
        self.location = x, y
        self.draw()

    def draw(self):
        # load image and set its location
        self.img = pygame.image.load(self.img_path)
        self.img_location = self.img.get_rect()
        self.img_location.center = self.location

    def update_position(self):
        self.img_location.centery += 5
        if self.img_location.top > screen_height:
            self.img_location.bottom = 0

class Truck(Vehicle):
    def __init__(self, x, y, truck = "vehicles/truck_tractor"):
        super().__init__()
        self.img_path = truck + ".png"
        self.location = x, y
        self.draw()

class Police(Vehicle):
    def __init__(self, x, y):
        super().__init__()
        self.img_path = "vehicles/police_car.png"
        self.location = x, y
        self.draw()

def isOverlapping(y, y_list, min_distance):
    for i in y_list:
        if abs(y - i) < min_distance:
            return True
    return False

# pygame settings
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Road")

background_image = pygame.image.load("road/road.png")

running = True

cars = []

# This Values can be adjusted
x_max_left_position  = (screen_width * (0.25))
x_max_right_position = (screen_width * (0.80))
y_position = 0

min_distance = 250  # Minimum distance between cars

for i in range(number_of_cars):
    x_position = random.randint(x_max_left_position, x_max_right_position)
    # y_position = random.randint(0, screen_height)
    y_position = 0

    vehicle_class = random.choice(["car","truck","police"])

    if vehicle_class == "car":
        c = random.choice(["red", "green", "blue"]) # colour
        cars.append(Vehicle(c, x_position, y_position))

    elif vehicle_class == "truck":
        k = random.choice(["vehicles/truck_tractor", "vehicles/box_truck"]) # kind
        cars.append(Truck(x_position, y_position, k))

    elif vehicle_class == "police":
        cars.append(Police(x_position, y_position))


# start game loop
while running:
    # if we click on the "exit" button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # stop game loop
            running = False

    for car in cars:
        car.update_position()

    # set background image
    screen.blit(background_image, (0, 0))

    # place images of cars
    for car in cars:
        screen.blit(car.img, car.img_location)

    pygame.display.flip()

pygame.quit()
