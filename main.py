from src.algorithm import *
from src.game import *

import time
import tkinter as tk
from functools import partial
import numpy as np
import matplotlib.pyplot as plt

def call_result(label_result, n1, n2):
    """
    ฟังก์ชันสำหรับการคำนวณผลลัพธ์และอัปเดต label ในหน้าต่าง Tkinter

    Parameters:
    label_result (tk.Label): Label ที่จะแสดงผลลัพธ์
    n1 (tk.StringVar): ค่าประชากรที่ป้อน
    n2 (tk.StringVar): จำนวนผู้สืบทอดที่ป้อน
    """
    global num1, num2
    num1 = n1.get()
    num2 = n2.get()
    result = int(num1) + int(num2)
    label_result.config(text=f"จำนวนประชากร = {num1} \n จำนวนผู้สืบทอด = {num2} \n\n (กรุณากดปิดหน้าตานี้)")
    return

# ค่าเริ่มต้นของ num1 และ num2
num1, num2 = 0, 0

# สร้างหน้าต่าง Tkinter สำหรับรับค่าจำนวนประชากรและจำนวนผู้สืบทอด
for _ in range(1):
    root = tk.Tk()
    root.geometry('400x200+100+200')
    root.title('Calculator')
    number1 = tk.StringVar()
    number2 = tk.StringVar()

    tk.Label(root, text="sol_per_pop").grid(row=1, column=0)
    tk.Label(root, text="num_generations").grid(row=3, column=0)
    tk.Entry(root, textvariable=number1).grid(row=1, column=2)
    tk.Entry(root, textvariable=number2).grid(row=3, column=2)
    
    labelResult = tk.Label(root)
    labelResult.grid(row=7, column=2)
    
    call_result_partial = partial(call_result, labelResult, number1, number2)
    tk.Button(root, text="กดเพิ่มยืนยันข้อมูล", command=call_result_partial).grid(row=10, column=0)
    
    root.mainloop()

# กำหนดค่าเริ่มต้น
sol_per_pop = int(num1)  # จำนวนประชากร
num_generations = int(num2)  # จำนวนรุ่นสืบทอด
snake_motion = 10
num_weights = valur_NN  # น้ำหนักของ NN W0 W1 W2 W3
plotdatagameY = []
plotdataaverage = []
plotdatagameX = []
MS = 0
SC = 0

# กำหนดขนาดของประชากร
pop_size = (sol_per_pop, num_weights)

# สร้างประชากรเริ่มต้น
new_population = np.random.choice(np.arange(-1, 1, step=0.01), size=pop_size, replace=True)
t_start = time.time()

num_parents_mating = int(sol_per_pop / 3.3)

# เริ่มการคำนวณแต่ละรุ่น
for generation in range(num_generations):
    print(f'##############        GENERATION {generation}  ###############')
    
    # วัดค่า fitness ของแต่ละโครโมโซมในประชากร
    fitness, MS, SC, datagamegen = cal_pop_fitness(new_population, NN_S, snake_motion, display_width, display_height, MS, SC)
    
    # บันทึกข้อมูลสำหรับการแสดงกราฟ
    plotdatagameY.append(max(datagamegen))
    plotdataaverage.append(np.average(datagamegen))
    plotdatagameX.append(generation)
    
    # แสดงกราฟเมื่อจบรอบสุดท้าย
    if generation == (num_generations - 1):
        t_end = time.time()
        fig = plt.figure()
        plt.plot(plotdatagameX, plotdatagameY, c='r')
        plt.plot(plotdatagameX, plotdataaverage, c='g')
        plt.title(f'Time Run model is : {int((t_end - t_start) / 60)}.{int((t_end - t_start) % 60)} minute')
        plt.ylabel('Score')
        plt.xlabel('Generation')
        plt.show()
        fig.savefig(f"Generation{MS}.png", dpi=fig.dpi, bbox_inches='tight', pad_inches=0.5)
        
        window = tk.Tk()
        window.title('Max Score of Snake Game')
        window.geometry("300x200+10+10")
        lbl = tk.Label(window, text=f"Max Score is {MS}", fg='red', font=("Helvetica", 16))
        lbl.pack()
        lb2 = tk.Label(window, text=f'Generations {num_generations} and sol per pop {sol_per_pop}', font=("Helvetica", 12))
        lb2.pack()
        lb3 = tk.Label(window, text=f'Time Run model is : {t_end - t_start:.2f} seconds', font=("Helvetica", 12))
        lb3.pack()
        window.mainloop()
    
    # เลือกพ่อแม่ที่ดีที่สุดในประชากรสำหรับการผสมพันธุ์
    parents = select_mating_pool(new_population, fitness, num_parents_mating)
    
    # สร้างรุ่นถัดไปโดยใช้ crossover
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
    
    # เพิ่มการกลายพันธุ์ให้กับลูกที่ถูกสร้าง
    offspring_mutation = mutation(offspring_crossover)
    
    # สร้างประชากรใหม่โดยอิงจากพ่อแม่และลูกที่ถูกกลายพันธุ์
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation
