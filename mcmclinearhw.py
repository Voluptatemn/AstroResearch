import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import threading

# reading the data, can be directly written in. 
x = []
y = []
yerr = []

with open('linear_data', 'r') as file:
     for line in file:
        data = [float(Decimal(number)) for number in line.split()]
        x.append(data[0])
        y.append(data[1])
        yerr.append(data[2])

x = np.array(x)
y = np.array(y)
yerr = np.array(yerr)

print("Reading finished.")

def plot_error(x, y, yerr):
    # Plotting with error bars
    plt.errorbar(x, y, yerr=yerr, fmt='o', label='Data with Error Bars')

    # Adding labels and title
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot with Error Bars')

    # Displaying legend
    plt.legend()

    # Display the plot
    plt.show()

# linear posterior space 
# posterior = p({x, y, sigma} | {m, b}) * p({m, b}) / p({x, y, sigma})
# -2 ln p({x, y, sigma} | {m, b}) = np.sum((y - M) ** 2 / sigma) = chisquare 
# excluded constant term and pos of model and pos of data 

def possibility_of_data_given_model(m, b, x = x, y = y, yerr = yerr):
    
    y_model = x * m + b
    return -1/2 * np.sum(((y - y_model) ** 2) / (yerr ** 2))

# posterior space visualization
def posterior_space_visualization():

    ms = []
    bs = []
    posterior = []

    for m in range (-100, 100):
        for b in range(-100, 100):
            ms.append(m)
            bs.append(b)
            posterior.append(possibility_of_data_given_model(m, b))

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(ms, bs, posterior, c='r', marker='o')

    # Adding labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')

    # Display the plot
    plt.show()

# metropolis-hasting
def metropolis_hasting(start_pointing, counts = {}, m_std = 1, b_std = 1, tracktor_upper_limit = 10 ** 8):

    current_pointing = start_pointing
    
    for i in tqdm(range(tracktor_upper_limit), desc="Processing items"):
        
        m = current_pointing[0]
        b = current_pointing[1]
        previous = possibility_of_data_given_model(m, b)
        
        # draw form distribution for interval
        # change the m and b 
        aftter_pointing = [np.random.normal(m, m_std), np.random.normal(b, b_std)]
        after = possibility_of_data_given_model(aftter_pointing[0], aftter_pointing[1])
        
        # acceptance prob
        acceptance_prob = np.min([1.0, previous/after])

        if np.random.choice([True, False], p=[acceptance_prob, 1-acceptance_prob]):
            # if accept
            aftter_pointing_tuple = tuple(aftter_pointing)
            if aftter_pointing_tuple in counts:
                counts[aftter_pointing_tuple] += 1
            else:
                counts[aftter_pointing_tuple] = 1
            current_pointing = aftter_pointing 
        else:
            current_pointing_tuple = tuple(current_pointing)
            if current_pointing_tuple in counts:
                counts[current_pointing_tuple] += 1
            else:
                counts[current_pointing_tuple] = 1

    print("Metropolis fasting complete")
    return current_pointing, counts

def metropolis_hasting_init(start_pointing, tracktor_upper_limit = 10 ** 8, walker_count = 10):
    
    tracktor_upper_limit / 10 

def metropolis_hasting(m, b, m_array = [], b_array = [], m_std = 1, b_std = 1, tracktor_upper_limit = 10 ** 8, walker_count = 10):

    for i in tqdm(range(tracktor_upper_limit), desc="Processing items"):
        
        previous = possibility_of_data_given_model(m, b)
        
        # draw form distribution for interval
        # change the m and b 
        after_m = np.random.normal(m, m_std)
        after_b = np.random.normal(b, b_std)
        after = possibility_of_data_given_model(after_m, after_b)
        
        # acceptance prob
        acceptance_prob = np.min([1.0, previous/after])

        if np.random.choice([True, False], p=[acceptance_prob, 1-acceptance_prob]):
            # if accept
            m = after_m
            b = after_b
            
        m_array.append(m)
        b_array.append(b)

    print("Metropolis fasting complete")
    return m, b, m_array, b_array

# finding max in counts dict
def find_max(counts):
    curr_max = 0
    position = []
    for key in counts.keys():
        frequency = counts[key]
        if frequency > curr_max:
            position = key
            curr_max = frequency
    return position, curr_max

# start metroplolis hasting, took around 1h 30 min
start_pointing = np.array((2.0, 5.0))
curr_pointing, counts = metropolis_hasting(start_pointing)
m, b, m_array, b_array = metropolis_hasting(start_pointing[0], start_pointing[1])
position, curr_max = find_max(counts)
print(position, curr_max)

def index_data_plot(data):
    # Plotting the graph
    plt.plot(data)

    # Adding labels to the axes
    plt.xlabel('Index')
    plt.ylabel('Data')

    # Adding a title to the plot
    plt.title('Index vs Data')

    # Display the plot
    plt.show()

start_pointing = [2.416905312902787, 3.9074407035248218]

def linear_model(x, m = start_pointing[0], b = start_pointing[1]):
    return m*x + b

# Plotting with error bars
plt.errorbar(x, y, yerr=yerr, fmt='o', label='Data with Error Bars')
x_fit = np.linspace(min(x), max(x), 100)
y_fit = linear_model(x_fit)
plt.plot(x_fit, y_fit, label='Fit', color='red')

# Adding labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Plot with Error Bars')

# Displaying legend
plt.legend()

# Display the plot
plt.show()





        


