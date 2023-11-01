import numpy as np
import matplotlib.pyplot as plt

'''
3x + 1, two visualization, leading digits into histogram, and the amount of steps it takes to get to 1
'''

def threeXPlusOne(x, step, sequence):
    sequence.append(x)
    step += 1
    if x == 1:
        return step, sequence
    if x % 2 == 0:
        x /= 2
        x = np.int64(x)
    else: 
        x = x * 3 + 1
    return threeXPlusOne(x, step, sequence)

def threeXPlusOne_outer(x):
    sequence = []
    step, sequence = threeXPlusOne(x, 0, sequence)
    return step, sequence

def list_index(list):
    my_list = []
    for i in range(len(list)):
        my_list.append(len(list) - i)
    return my_list

def plot_steps(times):
    for i in range(1, times+1):
        step, sequence = threeXPlusOne_outer(i)
        plt.scatter(list_index(sequence), sequence)
    plt.show()

plot_steps(30)

