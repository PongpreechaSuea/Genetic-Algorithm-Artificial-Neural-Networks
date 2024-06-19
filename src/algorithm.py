# genetic_algorithm

import numpy as np
import random
from random import randint
from src.run import run_game_with_ML
from src.config import display, clock

def cal_pop_fitness(pop, NN_S, snake_motion, display_width, display_height, MS, SC):
    """
    คำนวณค่า fitness ของประชากรแต่ละตัว โดยเล่นเกมด้วยน้ำหนักที่กำหนดในแต่ละโครโมโซม
    
    Parameters:
    pop (np.ndarray): ประชากรของโครโมโซม
    NN_S (list): ข้อมูลที่จำเป็นสำหรับ Neural Network
    snake_motion (int): การเคลื่อนไหวของงู
    display_width (int): ความกว้างของหน้าจอ
    display_height (int): ความสูงของหน้าจอ
    MS (?): ข้อมูลเกี่ยวกับคะแนนสูงสุด
    SC (?): ข้อมูลเกี่ยวกับคะแนน

    Returns:
    tuple: ค่า fitness, MS, SC, และคะแนนสูงสุดในแต่ละโครโมโซม
    """
    fitness = []
    datagamegen = []
    for i in range(pop.shape[0]):
        fit, MS, SC, max_score = run_game_with_ML(display, clock, pop[i], NN_S, snake_motion, display_width, display_height, MS, SC)
        print(f'Fitness value of chromosome {i}: {fit} || Score in chromosome: {max_score}')
        fitness.append(fit)
        datagamegen.append(max_score)
    return np.array(fitness), MS, SC, datagamegen

def select_mating_pool(pop, fitness, num_parents):
    """
    เลือกพ่อแม่ที่ดีที่สุดในรุ่นปัจจุบันสำหรับการสร้างลูกในรุ่นต่อไป
    
    Parameters:
    pop (np.ndarray): ประชากรของโครโมโซม
    fitness (np.ndarray): ค่า fitness ของแต่ละโครโมโซม
    num_parents (int): จำนวนพ่อแม่ที่ต้องการเลือก

    Returns:
    np.ndarray: โครโมโซมของพ่อแม่ที่ถูกเลือก
    """
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999  # ทำให้ไม่ถูกเลือกอีก
    return parents

def crossover(parents, offspring_size):
    """
    สร้างลูกสำหรับรุ่นถัดไปจากพ่อแม่ที่ถูกเลือก
    
    Parameters:
    parents (np.ndarray): โครโมโซมของพ่อแม่ที่ถูกเลือก
    offspring_size (tuple): ขนาดของลูกที่ต้องการสร้าง

    Returns:
    np.ndarray: โครโมโซมของลูกที่ถูกสร้าง
    """
    offspring = np.empty(offspring_size)
    for k in range(offspring_size[0]):
        while True:
            parent1_idx = random.randint(0, parents.shape[0] - 1)
            parent2_idx = random.randint(0, parents.shape[0] - 1)
            if parent1_idx != parent2_idx:
                for j in range(offspring_size[1]):
                    if random.uniform(0, 1) < 0.3:
                        offspring[k, j] = parents[parent1_idx, j]
                    else:
                        offspring[k, j] = parents[parent2_idx, j]
                break
    return offspring

def mutation(offspring_crossover):
    """
    กลายพันธุ์ลูกที่ถูกสร้างจากการ crossover เพื่อรักษาความหลากหลายในประชากร
    
    Parameters:
    offspring_crossover (np.ndarray): โครโมโซมของลูกที่ถูกสร้างจากการ crossover

    Returns:
    np.ndarray: โครโมโซมของลูกที่ถูกกลายพันธุ์
    """
    for idx in range(offspring_crossover.shape[0]):
        for _ in range(25):
            i = randint(0, offspring_crossover.shape[1] - 1)
            random_value = np.random.choice(np.arange(-1, 1, step=0.01), size=(1), replace=False)
            offspring_crossover[idx, i] += random_value
    return offspring_crossover

