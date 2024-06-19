# Action GameSnake

import random
import math
import numpy as np
import pygame
from config import *

"""
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN -> button_direction = 2
UP -> button_direction = 3
"""

def display_snake(snake_position, display):
    """แสดงตำแหน่งของงูบนหน้าจอ."""
    for position in snake_position:
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(position[0], position[1], 10, 10))

def display_apple(apple_position, display):
    """แสดงตำแหน่งของแอปเปิ้ลบนหน้าจอ."""
    pygame.draw.rect(display, (0, 255, 255), pygame.Rect(apple_position[0], apple_position[1], 10, 10))

def starting_positions():
    """กำหนดตำแหน่งเริ่มต้นของงูและแอปเปิ้ล."""
    snake_start = [100, 100]
    snake_position = [[100, 100], [90, 100], [80, 100]]
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score = 0
    return snake_start, snake_position, apple_position, score

def apple_distance_from_snake(apple_position, snake_position):
    """คำนวณระยะห่างระหว่างแอปเปิ้ลกับงู."""
    return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))

def generate_snake(snake_start, snake_position, apple_position, button_direction, score, snake_motion):
    """อัพเดตตำแหน่งของงูและตรวจสอบการชนกับแอปเปิ้ล."""
    if button_direction == 1:
        snake_start[0] += snake_motion
    elif button_direction == 0:
        snake_start[0] -= snake_motion
    elif button_direction == 2:
        snake_start[1] += snake_motion
    else:
        snake_start[1] -= snake_motion

    if snake_start == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0, list(snake_start))
    else:
        snake_position.insert(0, list(snake_start))
        snake_position.pop()
    return snake_position, apple_position, score

def collision_with_apple(apple_position, score):
    """ตรวจสอบและอัพเดตตำแหน่งของแอปเปิ้ลเมื่อถูกกิน."""
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    score += 1
    return apple_position, score

def collision_with_boundaries(snake_start, display_width, display_height):
    """ตรวจสอบการชนกับขอบเขตของจอ."""
    if (snake_start[0] >= display_width or snake_start[0] < 0 or
        snake_start[1] >= display_height or snake_start[1] < 0):
        return True
    return False

def collision_with_self(snake_start, snake_position):
    """ตรวจสอบการชนกับตัวเอง."""
    if snake_start in snake_position[1:]:
        return True
    return False

def blocked_directions(snake_position, display_width, display_height):
    """ตรวจสอบทิศทางที่ถูกบล็อค."""
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    is_front_blocked = is_direction_blocked(snake_position, current_direction_vector, display_width, display_height)
    is_left_blocked = is_direction_blocked(snake_position, left_direction_vector, display_width, display_height)
    is_right_blocked = is_direction_blocked(snake_position, right_direction_vector, display_width, display_height)

    return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

def is_direction_blocked(snake_position, direction_vector, display_width, display_height):
    """ตรวจสอบทิศทางที่ถูกบล็อค."""
    next_step = snake_position[0] + direction_vector
    if (collision_with_boundaries(next_step.tolist(), display_width, display_height) or
        collision_with_self(next_step.tolist(), snake_position)):
        return True
    return False

def generate_random_direction(snake_position, angle_with_apple):
    """สร้างทิศทางการเคลื่อนที่แบบสุ่ม."""
    direction = 0
    if angle_with_apple > 0:
        direction = 1
    elif angle_with_apple < 0:
        direction = -1
    return direction_vector(snake_position, angle_with_apple, direction)

def direction_vector(snake_position, angle_with_apple, direction):
    """คำนวณทิศทางการเคลื่อนที่ใหม่."""
    current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
    left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
    right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

    new_direction = current_direction_vector
    if direction == -1:
        new_direction = left_direction_vector
    elif direction == 1:
        new_direction = right_direction_vector

    button_direction = generate_button_direction(new_direction)
    return direction, button_direction

def generate_button_direction(new_direction):
    """แปลงทิศทางการเคลื่อนที่เป็นค่าปุ่มกด."""
    button_direction = 0
    if new_direction.tolist() == [10, 0]:
        button_direction = 1
    elif new_direction.tolist() == [-10, 0]:
        button_direction = 0
    elif new_direction.tolist() == [0, 10]:
        button_direction = 2
    else:
        button_direction = 3
    return button_direction

def angle_with_apple(snake_position, apple_position):
    """คำนวณมุมระหว่างงูกับแอปเปิ้ล."""
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_apple = np.linalg.norm(apple_direction_vector)
    norm_snake = np.linalg.norm(snake_direction_vector)
    norm_apple = 10 if norm_apple == 0 else norm_apple
    norm_snake = 10 if norm_snake == 0 else norm_snake

    apple_direction_vector_normalized = apple_direction_vector / norm_apple
    snake_direction_vector_normalized = snake_direction_vector / norm_snake

    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] -
        apple_direction_vector_normalized[0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] +
        apple_direction_vector_normalized[0] * snake_direction_vector_normalized[0]
    ) / math.pi

    return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized

def play_game(snake_start, snake_position, apple_position, button_direction, score, display, clock, snake_motion):
    """เล่นเกม."""
    crashed = False
    while not crashed:
        snake_position, apple_position, score = generate_snake(
            snake_start, snake_position, apple_position, button_direction, score, snake_motion)
        return snake_position, apple_position, score

def max_end_score(score, maxscore):
    """อัพเดตคะแนนสูงสุด."""
    if score > maxscore:
        maxscore = score
    return score, maxscore

# Example usage (commented out for running in a non-interactive environment):
# pygame.init()
# display = pygame.display.set_mode((500, 500))
# clock = pygame.time.Clock()
# snake_start, snake_position, apple_position, score = starting_positions()
# button_direction = 1  # Example direction
# snake_motion = 10  # Example motion step
# snake_position, apple_position, score = play_game(
#     snake_start, snake_position, apple_position, button_direction, score, display, clock, snake_motion)
# pygame.quit()
