import pygame
import sys, os
from enum import Enum

"""
Currently it only supports images of same size or grid gets weird, but hey

"""
class HighlightShape(Enum):
    Rect = 1,
    Circ = 2,
    NoHL = 3

# Initialize Pygame
pygame.init()

# Constants
IMAGES_WIDTH = 250
IMAGES_ACROSS = 5
MARGIN_H, MARGIN_W = 30,30
HIGHLIGHT_COLOR = (191, 182, 56)  # Gold color for the highlight
HIGHLIGHT_THICKNESS = 10
HIGHLIGHT_SHAPE = HighlightShape.Circ


#Default set by image width and Across 
SCREEN_WIDTH = (IMAGES_WIDTH+MARGIN_W)*IMAGES_ACROSS+MARGIN_W
SCREEN_HEIGHT = 850

clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Highlight Characters')

# Load the images image1-image9
D_IMAGES= {
    pygame.K_KP1: pygame.image.load(os.path.join('images',f'nobles (1).png')).convert_alpha(),
    pygame.K_KP2: pygame.image.load(os.path.join('images',f'nobles (2).png')).convert_alpha(),
    pygame.K_KP3: pygame.image.load(os.path.join('images',f'nobles (3).png')).convert_alpha(),
    pygame.K_KP4: pygame.image.load(os.path.join('images',f'nobles (7).png')).convert_alpha(),
    pygame.K_KP5: pygame.image.load(os.path.join('images',f'nobles (5).png')).convert_alpha(),
    pygame.K_KP6: pygame.image.load(os.path.join('images',f'nobles (6).png')).convert_alpha(),
    pygame.K_KP7: pygame.image.load(os.path.join('images',f'nobles (4).png')).convert_alpha(),
    pygame.K_KP8: pygame.image.load(os.path.join('images',f'nobles (8).png')).convert_alpha(),
    pygame.K_KP9: pygame.image.load(os.path.join('images',f'nobles (9).png')).convert_alpha(),
    pygame.K_1: pygame.image.load(os.path.join('images',f'nobles (10).png')).convert_alpha(),
    pygame.K_2: pygame.image.load(os.path.join('images',f'nobles (11).png')).convert_alpha(),
    pygame.K_3: pygame.image.load(os.path.join('images',f'nobles (12).png')).convert_alpha(),
    pygame.K_4: pygame.image.load(os.path.join('images',f'nobles (13).png')).convert_alpha()
}

for key, img in D_IMAGES.items():
    h, w = img.get_size()
    aspect_ratio = h/w
    scaled_image = pygame.transform.scale(img,(IMAGES_WIDTH, IMAGES_WIDTH*aspect_ratio))
    D_IMAGES[key] = scaled_image

# Main loop flags
running = True

# Functions
def arrange_images(image_dict:dict = D_IMAGES):
    positions = {}
    w_mult = 0
    h_mult = 0
    count = 0

    for key, img in image_dict.items():
        h, w = img.get_size()
        aspect_ratio = h/w

        x = MARGIN_W + (MARGIN_W + IMAGES_WIDTH) * w_mult
        y = MARGIN_H + (MARGIN_H + IMAGES_WIDTH*aspect_ratio) * h_mult
        screen.blit(img, (x, y))
        positions.update({key:(x,y)})
        w_mult += 1

        if w_mult == IMAGES_ACROSS:
            w_mult = 0
            h_mult += 1

    return positions

def add_rect_highlight(image, pos):
    if image is not None and pos is not None:
        rect = image.get_rect(topleft=pos)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, HIGHLIGHT_THICKNESS)

def add_circ_highlight(image, pos):
    if image is not None and pos is not None:
        rect = image.get_rect(topleft=pos)
        center = rect.center
        radius = max(rect.width, rect.height) // 2
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, center, radius, HIGHLIGHT_THICKNESS)

        

fullscreen = False
current_image = None
current_position = None

# Main loop
while running:

    clock.tick(60)
    keys = pygame.key.get_pressed()

    # Key Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            if event.key in D_IMAGES:
                # print("Tru")
                current_image = D_IMAGES[event.key]
                current_position = positions[event.key]
                # print(current_image)
                # print(current_position)

            if event.key == pygame.K_KP0:
                current_image = None

            if event.key == pygame.K_f:
                # Toggle fullscreen
                if fullscreen:
                    DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    fullscreen = False
                else:
                    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    fullscreen = True
            
                

    # Fill the screen and add images
    screen.fill((0, 0, 0))
    positions = arrange_images()

    # Transparency
    for key, pos in positions.items():
        image = D_IMAGES[key]
        if image != current_image:
            image.set_alpha(80)
        else:
            image.set_alpha(225)
            screen.blit(image, pos)

    if HIGHLIGHT_SHAPE == HighlightShape.Rect:            
        add_rect_highlight(current_image,current_position)
    elif HIGHLIGHT_SHAPE == HighlightShape.Circ:
        add_circ_highlight(current_image,current_position)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
