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
    for i in range(1, len(list)+1):
        my_list.append(i)
    return my_list

def plot_steps(times):
    for i in range(1, times+1):
        step, sequence = threeXPlusOne_outer(i)
        plt.plot(list_index(sequence), sequence, '-o')
    plt.show()
    
def plot_hist(times):
    digit_counts = {digit: 0 for digit in range(1, 10)}
    for i in range(1, times+1):
        step, sequence = threeXPlusOne_outer(i)
        leading_digits = [int(str(abs(num))[0]) for num in sequence]
        digit_counts = {digit: digit_counts[digit] + leading_digits.count(digit) for digit in range(1, 10)}
    plt.bar(digit_counts.keys(), digit_counts.values())  
    plt.show()
            
plot_hist(100)



