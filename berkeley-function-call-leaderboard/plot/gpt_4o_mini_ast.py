import csv
import numpy as np
import matplotlib.pyplot as plt


performance_all = []

# calculate average performance across 8 test categories

random_select_nums = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]

for random_select_num in random_select_nums:
    data_overall = []
    with open(f"../score_{random_select_num}/data_overall.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data_overall.append(row)
    
    data_non_live = []
    with open(f"../score_{random_select_num}/data_non_live.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data_non_live.append(row)
    
    data_live = []
    with open(f"../score_{random_select_num}/data_live.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            data_live.append(row)
        
    py_ast_non_live_simple = float(data_non_live[1][5].rstrip('%'))
    py_ast_non_live_multiple = float(data_non_live[1][8].rstrip('%'))
    py_ast_non_live_parallel = float(data_non_live[1][9].rstrip('%'))
    py_ast_non_live_parallel_multiple = float(data_non_live[1][10].rstrip('%'))

    py_ast_live_simple = float(data_live[1][4].rstrip('%'))
    py_ast_live_multiple = float(data_live[1][5].rstrip('%'))
    py_ast_live_parallel = float(data_live[1][6].rstrip('%'))
    py_ast_live_parallel_multiple = float(data_live[1][7].rstrip('%'))

    avr_acc = float(
        py_ast_non_live_simple + 
        py_ast_non_live_multiple + 
        py_ast_non_live_parallel + 
        py_ast_non_live_parallel_multiple + 
        py_ast_live_simple + 
        py_ast_live_multiple + 
        py_ast_live_parallel + 
        py_ast_live_parallel_multiple
    ) / 8

    performance_all.append(avr_acc)


print(performance_all)

x_plot = [0.5 if x == 0 else x for x in random_select_nums]

plt.figure(figsize=(10, 6))
plt.semilogx(x_plot, performance_all, marker='o', linewidth=2, markersize=6)
plt.xlabel('number of additional functions (log scale)')
plt.ylabel('avr acc')

# Custom x-axis labels to show the real values
plt.xticks(x_plot, random_select_nums)
plt.grid(True, alpha=0.3)
plt.savefig('./accuracy_plot.png', dpi=300)