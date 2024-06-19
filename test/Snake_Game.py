import random
import time
import math
from tqdm import tqdm
import numpy as np
import pygame

def display_snake(snake_position, display):
    for position in snake_position:
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(position[0], position[1], 10, 10))


def display_apple(apple_position, display):
    pygame.draw.rect(display, (0, 255, 255), pygame.Rect(apple_position[0], apple_position[1], 10, 10))


def starting_positions():
    snake_start = [100, 100]
    snake_position = [[100, 100], [99, 100], [98, 100]]
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score = 0
    return snake_start, snake_position, apple_position, score

def apple_distance_from_snake(apple_position, snake_position):
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))

def generate_snake(snake_start, snake_position, apple_position, button_direction, score , snake_motion): #การเคลื่อนที่ของงู
    if button_direction == 1:
        snake_start[0] += snake_motion #10
    elif button_direction == 0:
        snake_start[0] -= snake_motion #10
    elif button_direction == 2:
        snake_start[1] += snake_motion #10
    else:
        snake_start[1] -= snake_motion #10

    if snake_start == apple_position:   #ถ้าตำแหน่งของงูและแอปเปิ้ลตรงกัน
        apple_position, score = collision_with_apple(apple_position, score)
        # snake_position.append([(snake_position[-1][0])-1, 100])
        snake_position.insert(0, list(snake_start))
        # print(len(snake_position))
        # print("Score : " + str(score))
    else: 
        snake_position.insert(0, list(snake_start))
        snake_position.pop()
    return snake_position, apple_position, score


def collision_with_apple(apple_position, score): #กิน
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score


def collision_with_boundaries(snake_start,display_width,display_height):  #ชนกำแพง
    if snake_start[0] >= display_width or snake_start[0] < 0 or snake_start[1] >= display_height or snake_start[1] < 0:
        return 1 
    else:
        return 0

def collision_with_self(snake_start, snake_position):  #ชนตัวเอง
    snake_start = snake_position[0]
    if snake_start in snake_position[1:]:
        return 1
    else:
        return 0


def blocked_directions(snake_position,display_width,display_height):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector,display_width,display_height)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector,display_width,display_height)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector,display_width,display_height)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked


def is_direction_blocked(snake_position, current_direction_vector ,display_width,display_height):
    next_step = snake_position[0] + current_direction_vector
    snake_start = snake_position[0]
    if collision_with_boundaries(next_step,display_width,display_height) == 1 or collision_with_self(next_step.tolist(), snake_position) == 1:
        return 1
    else:
        return 0


def generate_random_direction(snake_position, angle_with_apple):
    direction = 0
    if angle_with_apple > 0:
        direction = 1
    elif angle_with_apple < 0:
        direction = -1
    else:
        direction = 0

    return direction_vector(snake_position, angle_with_apple, direction)


def direction_vector(snake_position, angle_with_apple, direction):
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    new_direction = current_direction_vector

    if direction == -1:
        new_direction = left_direction_vector
    if direction == 1:
        new_direction = right_direction_vector

    button_direction = generate_button_direction(new_direction)

    return direction, button_direction


def generate_button_direction(new_direction,snake_motion):
    button_direction = 0
    if new_direction.tolist() == [snake_motion, 0]:
        button_direction = 1
    elif new_direction.tolist() == [-snake_motion, 0]:
        button_direction = 0
    elif new_direction.tolist() == [0, snake_motion]:
        button_direction = 2
    else:
        button_direction = 3

    return button_direction


def angle_with_apple(snake_position, apple_position):
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 10
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[0]) / math.pi
    return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized


def play_game(snake_start, snake_position, apple_position, button_direction, score, display, clock ,snake_motion):
    crashed = False
    while crashed is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
        display.fill((255, 255, 255))

        display_apple(apple_position, display)
        display_snake(snake_position, display)

        snake_position, apple_position, score = generate_snake(snake_start, snake_position, apple_position,
                                                               button_direction, score ,snake_motion)
        pygame.display.set_caption("SCORE: " + str(score))
        pygame.display.update()
        clock.tick(50000) #50000

        return snake_position, apple_position, score

def Maxend_score(score,maxscore):
    if score > maxscore:
        maxscore = score
        return score,maxscore
    else:
        return score,maxscore

'''
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN ->button_direction = 2
UP -> button_direction = 3
'''

display_width = 600
display_height = 600
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
white = (0,0,0)

pygame.init()
display=pygame.display.set_mode((display_width,display_height))
clock=pygame.time.Clock()


# display=0#pygame.display.set_mode((display_width,display_height))
# clock=0#pygame.time.Clock()