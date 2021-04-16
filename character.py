"""
This is the file that draws the character in the game
"""
import sys
from typing import Tuple
import pygame
from player import Player

pygame.init()
screen = pygame.display.set_mode((600, 800))
background = pygame.image.load('OIP.jpg').convert()
start = pygame.image.load('start.jpg').convert()
RUNNING = True
score = 0
pygame.display.set_caption('Treasure Hunt')
my_font = pygame.font.SysFont('arial', 60)
font = pygame.font.SysFont('arial', 40)

unit = 10
initial_pos = (200, 80)
treasure_pos = ...


class Char(Player):
    """
    the class of the character in the game
    """
    def __init__(self, user_id: str, initial_pos: Tuple[int, int], vision_field: int) -> None:
        super().__init__(user_id, initial_pos, vision_field)
        self.image = pygame.image.load('char.jpg')
        self.rect = self.image.get_rect()
        self.pos = initial_pos

    def move(self) -> None:
        """
        control the movement of the character
        """
        self.rect = self.rect.move()

    def possible_movement(self) -> Tuple[int, int]:
        """
        the possible movement the player could make at the current position

        Precondition:
         - self.move_up is True or self.move_down is True
         - self.move_left is True or self.move_right is True
        """
        ...
    def meet_obstacle(self, bool) -> None:
        ...

    def meet_treasure(self, bool) -> None:
        if bool == True:
            self.image = pygame.image.load('happy.jpg')
        else:
            return
        
class Treasure(pygame.sprite.Sprite):
    """
    the class of the treasures the hunter need to find
    """
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('treasure.jpg')
        self.rect = self.image.get_rect()
        self.pos = treasure_pos

char = Char('Yuta', initial_pos, 5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_LEFT]:
        # draw out the map
        # display the path char has taken
        # char move to the left
        # display possible next move

    if pressed_keys[pygame.K_RIGHT]:
        # draw out the map
        # display the path char has taken
        # char move to the left
        # display possible next move

    if pressed_keys[pygame.K_UP]:
        # draw out the map
        # display the path char has taken
        # char move up
        # display possible next move

    if pressed_keys[pygame.K_DOWN]:
        # draw out the map
        # display the path char has taken
        # char move down
        # display possible next move

    pygame.display.update()
