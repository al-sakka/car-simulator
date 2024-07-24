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
car_position = 150

# Speed of background scroll
background_min_speed    = 5
background_speed        = 15
background_max_speed    = 40
background_speed_offset = 5
stones = []
cars = []

# Place Pygame window at a specific location
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

# Classes
class Vehicle:
    def __init__(self, colour = "red", x = 400, y = car_position):
        self.img_path = "vehicles/" + colour + ".png"
        self.location = x, y
        self.draw()

    def draw(self):
        # Load image and set its location
        self.img = pygame.image.load(self.img_path)
        self.img_location = self.img.get_rect()
        self.img_location.center = self.location

    def move(self, position):
        if (position == "RIGHT") and (self.img_location.centerx + 5 <= x_max_right_position):
            self.img_location.x += 10
        elif (position == "LEFT") and (self.img_location.centerx - 5 >= x_max_left_position):
            self.img_location.x -= 10

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

class Stone:
    def  __init__(self, kind = "grass", x = 400, y = 300, size = (100,100)):
        self.img_path = "road/" + kind + ".png"
        self.location = x, y
        self.size = size
        self.draw()

    def draw(self):
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, self.size)  # Resize the image
        self.img_location = self.img.get_rect()
        self.img_location.center = self.location

    ##
    def update_position(self):
        self.img_location.centery -= background_speed
        if self.img_location.bottom < 0:
            stones.clear()
            grass_num = random.randint(1,2)
            for i in range(grass_num):
                x_position = random.randint(x_max_left_position, x_max_right_position)
                y_position = random.randint(0, screen_height)
                stones.append(Stone("grass", x_position, y_position))


# Pygame settings
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(label)

background_image = pygame.image.load("road/road.png")
running = True

# Initialize stones
for _ in range(10):  # Adjust number as needed
    x_position = random.randint(x_max_left_position, x_max_right_position)
    y_position = random.randint(0, screen_height)  # Start stones off-screen
    stones.append(Stone("grass", x_position, y_position))


for i in range(number_of_cars):
    x_position = random.randint(x_max_left_position, x_max_right_position)
    vehicle_class = random.choice(["car", "truck", "police"])

    if vehicle_class == "car":
        c = random.choice(["red", "green", "blue"])  # Colour
        cars.append(Vehicle(c, x_position, car_position))
    elif vehicle_class == "truck":
        k = random.choice(["vehicles/truck_tractor", "vehicles/box_truck"])  # Kind
        cars.append(Truck(x_position, car_position, k))
    elif vehicle_class == "police":
        cars.append(Police(x_position, car_position))

# Background positions
background_y1 = 0
background_y2 = screen_height

# Start game loop
while running:
    # If we click on the "exit" button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Stop game loop
            running = False

    # Check if any arrow keys are being held down
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_RIGHT]) or (keys[pygame.K_d]):
        for car in cars:
            car.move("RIGHT")
    if (keys[pygame.K_LEFT]) or (keys[pygame.K_a]):
        for car in cars:
            car.move("LEFT")
    if (keys[pygame.K_DOWN]) or (keys[pygame.K_s]) and (background_speed < background_max_speed):
        background_speed += background_speed_offset
    if (keys[pygame.K_UP]) or (keys[pygame.K_w]) and (background_speed > background_min_speed):
        background_speed -= background_speed_offset

    # Update background positions
    background_y1 -= background_speed
    background_y2 -= background_speed

    # Reset background positions
    if background_y1 <= -screen_height:
        background_y1 = screen_height
    if background_y2 <= -screen_height:
        background_y2 = screen_height

    for stone in stones:
        stone.update_position()

    # Set background image
    screen.blit(background_image, (0, background_y1))
    screen.blit(background_image, (0, background_y2))

    # Place Stones
    for stone in stones:
        screen.blit(stone.img, stone.img_location)

    # Place Cars
    for car in cars:
        screen.blit(car.img, car.img_location)

    pygame.display.flip()

pygame.quit()
