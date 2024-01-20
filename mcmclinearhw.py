import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm

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
    
    sum = 0
    for j in range (len(y)):
        sum += ((y[j] - (m * x[j] + b)) ** 2) / (yerr[j] ** 2)
    return -1/2 * sum
    
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
        previous = possibility_of_data_given_model(current_pointing[0], current_pointing[1])
        
        # draw form distribution for interval
        # change the m and b 
        aftter_pointing = [np.random.normal(current_pointing[0], m_std), np.random.normal(current_pointing[1], b_std)]
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
position, curr_max = find_max(counts)
print(position, curr_max)

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





        


