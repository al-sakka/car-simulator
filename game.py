import pygame
import random
import os

label = "Car Simulator"
screen_width = 800
screen_height = 600

# These values can be adjusted
x_max_left_position = int(screen_width * 0.25)
x_max_right_position = int(screen_width * 0.8)
car_position = 150

# Speed of background scroll
background_min_speed = 5
background_speed = 15
background_max_speed = 40
background_speed_offset = 5
stones = []
cars = []

# Maximum number of stones to show on screen
max_stones = 4

# Place Pygame window at a specific location
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

# Classes
class Vehicle:
    def __init__(self, colour="red", x=400, y=car_position):
        self.img_path = "vehicles/" + colour + ".png"
        self.location = x, y
        self.draw()

    def draw(self):
        # Load image and set its location
        self.img = pygame.image.load(self.img_path)
        self.img_location = self.img.get_rect()
        self.img_location.center = self.location

    def move(self, position):
        if position == "RIGHT" and self.img_location.centerx + 10 <= x_max_right_position:
            self.img_location.x += 10
        elif position == "LEFT" and self.img_location.centerx - 10 >= x_max_left_position:
            self.img_location.x -= 10

class Truck(Vehicle):
    def __init__(self, x, y):
        super().__init__(colour="red", x=x, y=y)
        self.img_path = "vehicles/box_truck.png"
        self.draw()

class Police(Vehicle):
    def __init__(self, x, y):
        super().__init__(colour="red", x=x, y=y)
        self.img_path = "vehicles/police_car.png"
        self.draw()

class Stone:
    def __init__(self, kind="grass", x=400, y=300, size=(100, 100)):
        self.img_path = "road/" + kind + ".png"
        self.location = x, y
        self.size = size
        self.draw()

    def draw(self):
        self.img = pygame.image.load(self.img_path)
        self.img = pygame.transform.scale(self.img, self.size)  # Resize the image
        self.img_location = self.img.get_rect()
        self.img_location.center = self.location

    def update_position(self):
        self.img_location.centery -= background_speed
        if self.img_location.bottom < 0:
            stones_to_remove.append(self)
            if len(stones) - len(stones_to_remove) < max_stones:
                x_position = random.randint(x_max_left_position, x_max_right_position)
                y_position = random.randint(screen_height, screen_height + 100)
                stones_to_add.append(Stone("grass", x_position, y_position))

# Pygame settings
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(label)

background_image = pygame.image.load("road/road.png")
arrows_icon = pygame.image.load("road/arrows.png")
arrows_icon = pygame.transform.scale(arrows_icon, (150, 150))
# background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
running = True

# Initialize stones
for _ in range(max_stones):  # Adjust number as needed
    x_position = random.randint(x_max_left_position, x_max_right_position)
    y_position = random.randint(0, screen_height)  # Start stones on-screen
    stones.append(Stone("grass", x_position, y_position))

x_position = random.randint(x_max_left_position, x_max_right_position)
vehicle_class = random.choice(["car", "truck", "police"])

if vehicle_class == "car":
    c = random.choice(["red", "green", "blue"])  # Colour
    cars.append(Vehicle(c, x_position, car_position))
elif vehicle_class == "truck":
    cars.append(Truck(x_position, car_position))
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
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        for car in cars:
            car.move("RIGHT")
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        for car in cars:
            car.move("LEFT")
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and background_speed < background_max_speed:
        background_speed += background_speed_offset
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and background_speed > background_min_speed:
        background_speed -= background_speed_offset

    # Update background positions
    background_y1 -= background_speed
    background_y2 -= background_speed

    # Reset background positions
    if background_y1 <= -screen_height:
        background_y1 = screen_height
    if background_y2 <= -screen_height:
        background_y2 = screen_height

    # Initialize lists to handle adding and removing stones
    stones_to_remove = []
    stones_to_add = []

    for stone in stones:
        stone.update_position()

    # Remove stones that have gone off-screen and add new stones
    for stone in stones_to_remove:
        stones.remove(stone)
    for stone in stones_to_add:
        stones.append(stone)

    # Set background image
    screen.blit(background_image, (0, background_y1))
    screen.blit(background_image, (0, background_y2))

    screen.blit(arrows_icon, (screen_width - 150, screen_height - 150))

    # Place Stones
    for stone in stones:
        screen.blit(stone.img, stone.img_location)

    # Place Cars
    for car in cars:
        screen.blit(car.img, car.img_location)

    pygame.display.flip()

pygame.quit()
