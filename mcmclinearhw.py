import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time 

start_time = time.time()

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

# # Plotting with error bars
# plt.errorbar(x, y, yerr=yerr, fmt='o', label='Data with Error Bars')

# # Adding labels and title
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')
# plt.title('Plot with Error Bars')

# # Displaying legend
# plt.legend()

# # Display the plot
# plt.show()

# linear posterior space 
# posterior = p({x, y, sigma} | {m, b}) * p({m, b}) / p({x, y, sigma})
# -2 ln p({x, y, sigma} | {m, b}) = np.sum((y - M) ** 2 / sigma) = chisquare 
possibility_of_model = 1

def possibility_of_data_given_model(m, b, x = x, y = y, yerr = yerr, fast_version = True):
    
    if fast_version:
        sum = 0
        for j in range (len(y)):
            sum += ((y[j] - (m * x[j] + b)) ** 2) / (yerr[j] ** 2)
        return np.e ** (-1/2 * sum)
    sum = 0
    for j in range (len(y)):
        sum += ((y[j] - (m * x[j] + b)) ** 2) / (yerr[j] ** 2) - np.log(yerr[j] * np.sqrt(2 * np.pi))
    return np.e ** (-1/2 * sum)
    
possibility_of_data = 1

def possibility_of_model_given_data(m, b):
    return possibility_of_model * possibility_of_data_given_model(m, b) / possibility_of_data

# ms = []
# bs = []
# posterior = []

# for m in range (-100, 100):
#     for b in range(-100, 100):
#         ms.append(m)
#         bs.append(b)
#         posterior.append(possibility_of_model_given_data(m, b))

# # Create a 3D plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Scatter plot
# ax.scatter(ms, bs, posterior, c='r', marker='o')

# # Adding labels
# ax.set_xlabel('X-axis')
# ax.set_ylabel('Y-axis')
# ax.set_zlabel('Z-axis')

# # Display the plot
# plt.show()

# metropolis-hasting
def metropolis_hasting(start_pointing, num_of_tracktors = 0, m_mean = 0, m_std = 1, b_mean = 0, b_std = 1, tracktor_upper_limit = 10 ** 8, fast_version = True):
    counts = {}
    current_pointing = start_pointing
    while (num_of_tracktors < tracktor_upper_limit):
        num_of_tracktors += 1
        
        if fast_version:
            if num_of_tracktors % 1000000 == 0:
                print(num_of_tracktors)
        else:
            print(num_of_tracktors)
        previous = possibility_of_model_given_data(current_pointing[0], current_pointing[1])
        
        # draw form distribution for interval 
        m_move = np.random.normal(m_mean, m_std)
        b_move = np.random.normal(b_mean, b_std)
        
        # change the m and b
        aftter_pointing = current_pointing + (m_move, b_move)
        after = possibility_of_model_given_data(aftter_pointing[0], aftter_pointing[1])
        
        # acceptance prob
        acceptance_prob = np.min([1.0, after/previous])

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
    return counts

start_pointing = np.array((2.0, 5.0))
counts = metropolis_hasting(start_pointing)
curr_max = 0
position = []
for key in counts.keys():
    frequency = counts[key]
    if frequency > curr_max:
        position = key
        curr_max = frequency
print(position, curr_max)

end_time = time.time()
elapsed_time_seconds = end_time - start_time
elapsed_minutes = int(elapsed_time_seconds // 60)
elapsed_seconds = int(elapsed_time_seconds % 60)
print(f"Job time: {elapsed_minutes} minutes and {elapsed_seconds} seconds")    








        


