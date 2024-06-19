# Training-Snake-Game-Using-Genetic-Algorithm

This project implements a Snake Game that uses a Genetic Algorithm to optimize the neural network controlling the snake. The goal is to evolve the snake's behavior to maximize its score by eating apples and avoiding collisions.

This project leverages data for development in various fields and is designed for educational and learning purposes.

This project was developed by students from Panyapiwat Institute of Management.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Genetic Algorithm](#genetic-algorithm)
- [Game Mechanics](#game-mechanics)
- [Visualization](#visualization)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/PongpreechaSuea/Genetic-Algorithm-Artificial-Neural-Networks.git
    cd snake-genetic-algorithm
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the game with genetic algorithm:**
    ```sh
    python main.py
    ```

2. **Input Parameters:**
    - `sol_per_pop`: Number of solutions per population.
    - `num_generations`: Number of generations for the genetic algorithm.

    These parameters will be prompted via a Tkinter interface at the start of the program.

## Project Structure

```
    .
    ├── src
    │ ├── algorithm.py # Genetic algorithm functions
    | ├── config.py # Configuration constants
    │ ├── game.py # Snake game functions
    | ├── network.py # Feed_Forward_Neural_Network 
    │ └── run.py # Functions to run the game with ML model
    ├── main.py # Main script to run the project
    ├── requirements.txt # Python dependencies
    └── README.md # Project documentation
```

## Configuration

Edit the `config.py` file to change game settings and neural network parameters:

```python
# config.py

# Game settings
display_width = 500
display_height = 500

# Neural network settings
NN_S = ...  # Size of the neural network
valur_NN = ...  # Number of weights in the neural network
```

## Genetic Algorithm
The genetic algorithm includes the following steps:

1. Initialization: Create an initial population of neural network weights.
2. Fitness Calculation: Evaluate the fitness of each individual in the population by running the snake game and recording the score.
3. Selection: Select the best-performing individuals to be parents for the next generation.
4. Crossover: Create offspring by combining the weights of two parents.
5. Mutation: Introduce random changes to some offspring to maintain diversity in the population.
6. Repeat: The process is repeated for a defined number of generations.


## Game Mechanics
- Snake Movement: The snake moves based on the outputs of the neural network.
- Apple Consumption: The snake grows longer and the score increases when it eats an apple.
- Collision Detection: The game ends if the snake collides with the boundaries or itself.

## Visualization
After the genetic algorithm finishes running, the results are visualized using matplotlib:

- Max Score per Generation: The maximum score achieved by any individual in each generation.
- Average Score per Generation: The average score of all individuals in each generation.
A Tkinter window displays the final maximum score and run time.
