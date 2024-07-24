import pygame
import random
import os

label = "Car Simulator"
number_of_cars = 1
screen_width = 800
screen_height = 600

# These values can be adjusted
x_max_left_position = int(screen_width * 0.25)
x_max_right_position = int(screen_width * 0.8)
y_position = 150

# Place Pygame window at a specific location
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

# Classes
class Vehicle:
    def __init__(self, colour="red", x=400, y=400):
        self.img_path = "vehicles/" + colour + ".png"
        self.location = x, y
        self.draw()

    def draw(self):
        # Load image and set its location
        self.img = pygame.image.load(self.img_path)
        self.img_location = self.img.get_rect()
        self.img_location.center = self.location

    def update_position(self):
        self.img_location.centery -= 5
        if self.img_location.bottom < 0:
            self.img_location.top = screen_height

    def move(self, position):
        if (position == 1) and (self.img_location.centerx + 5 <= x_max_right_position):
            self.img_location.x += 5
        elif (position == 2) and (self.img_location.centerx - 5 >= x_max_left_position):
            self.img_location.x -= 5

class Truck(Vehicle):
    def __init__(self, x, y, truck="vehicles/truck_tractor"):
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

# Pygame settings
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(label)

background_image = pygame.image.load("road/road.png")

running = True

cars = []

for i in range(number_of_cars):
    x_position = random.randint(x_max_left_position, x_max_right_position)
    vehicle_class = random.choice(["car", "truck", "police"])

    if vehicle_class == "car":
        c = random.choice(["red", "green", "blue"])  # Colour
        cars.append(Vehicle(c, x_position, y_position))
    elif vehicle_class == "truck":
        k = random.choice(["vehicles/truck_tractor", "vehicles/box_truck"])  # Kind
        cars.append(Truck(x_position, y_position, k))
    elif vehicle_class == "police":
        cars.append(Police(x_position, y_position))

# Background positions
background_y1 = 0
background_y2 = screen_height

# Speed of background scroll
background_speed = 20

# Start game loop
while running:
    # If we click on the "exit" button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stop game loop
            running = False

    # Check if any arrow keys are being held down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        for car in cars:
            car.move(1)
    if keys[pygame.K_LEFT]:
        for car in cars:
            car.move(2)
    if (keys[pygame.K_DOWN]) and (background_speed < 40):
        background_speed += 5
    if (keys[pygame.K_UP]) and (background_speed > 5):
        background_speed -= 5


    # for car in cars:
    #     car.update_position()

    # Update background positions
    background_y1 -= background_speed
    background_y2 -= background_speed

    # Reset background positions
    if background_y1 <= -screen_height:
        background_y1 = screen_height
    if background_y2 <= -screen_height:
        background_y2 = screen_height

    # Set background image
    screen.blit(background_image, (0, background_y1))
    screen.blit(background_image, (0, background_y2))

    # Place images of cars
    for car in cars:
        screen.blit(car.img, car.img_location)

    pygame.display.flip()

pygame.quit()
