from src.game import *
from src.network import *

def run_game_with_ML(display, clock, weights,NN_S,snake_motion,display_width,display_height, MS , SC):
    max_score = 0
    avg_score = 0
    test_games = 1
    score1 = 0
    score2 = 0
    if MS <= 4 :
        steps_per_game = 150
    elif MS > 3 and MS <= 15:
        steps_per_game = 1500
    elif MS > 15 and MS <= 25:
        steps_per_game = 2500 #2500
    else:
        steps_per_game = int(MS*100) #int(((MS+1)/2)*500)
    

    for _ in range(test_games):
        snake_start, snake_position, apple_position, score = starting_positions()
        
        count_same_direction = 0
        prev_direction = 0

        for _ in range(steps_per_game):
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(
                snake_position,display_width,display_height)
            angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(
                snake_position, apple_position)
            predictions = []
            predicted_direction = np.argmax(np.array(forward_propagation(np.array(
                [is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 7), weights , NN_S))) - 1

            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction

            new_direction = np.array(snake_position[0]) - np.array(snake_position[1])
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            if predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            button_direction = generate_button_direction(new_direction,snake_motion)

            next_step = snake_position[0] + current_direction_vector
            if collision_with_boundaries(snake_position[0],display_width,display_height) == 1 or collision_with_self(next_step.tolist(),snake_position) == 1:
                score1 += -150
                break
            else:
                score1 += 0

            snake_position, apple_position, score = play_game(
                snake_start, 
                snake_position, 
                apple_position,
                button_direction, 
                score, 
                display, 
                clock , 
                snake_motion
            )

            if score > max_score:
                max_score = score
            SC , MS = max_end_score(score,MS)
            if count_same_direction > 8 and predicted_direction != 0:
                score2 -= 1
            else:
                score2 += 2

    return score1 + score2 + ( max_score * 5000 ), MS , SC , max_score
