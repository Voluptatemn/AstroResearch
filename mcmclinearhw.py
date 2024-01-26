import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt
from tqdm import tqdm
import concurrent.futures

# author : sw
# data of submission: 1-24-2024
# took around 1h for list without parrellal, 16 minutes with
class MCMC:

    def __init__(self):
        self.read_data()
        self.start_pointing = [2.4917059853078456, 3.2155451588701913]

    def read_data(self):
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

        self.x = np.array(x)
        self.y = np.array(y)
        self.yerr = np.array(yerr)

        print("Reading finished.")

    def plot_error(self):
        # Plotting with error bars
        plt.errorbar(self.x, self.y, yerr=self.yerr, fmt='o', label='Data with Error Bars')

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

    def possibility_of_data_given_model(self, m, b):
        
        y_model = self.x * m + b
        return np.e ** (-1/2 * np.sum(((self.y - y_model) ** 2) / (self.yerr ** 2)))

    # posterior space visualization
    def posterior_space_visualization(self):

        ms = []
        bs = []
        posterior = []

        for m in range (-100, 100):
            for b in range(-100, 100):
                ms.append(m)
                bs.append(b)
                posterior.append(self.possibility_of_data_given_model(m, b))

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

    # metropolis-hasting, dictionary way
    def metropolis_hasting_dict(self, start_pointing, counts = {}, m_std = 1, b_std = 1, tracktor_upper_limit = 10 ** 8):

        current_pointing = start_pointing
        
        for i in tqdm(range(tracktor_upper_limit), desc="Processing items"):
            
            m = current_pointing[0]
            b = current_pointing[1]
            previous = self.possibility_of_data_given_model(m, b)
            
            # draw form distribution for interval
            # change the m and b 
            aftter_pointing = [np.random.normal(m, m_std), np.random.normal(b, b_std)]
            after = self.possibility_of_data_given_model(aftter_pointing[0], aftter_pointing[1])
            
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

    # parrellal run attempt
    def metropolis_hasting_init(self, m, b, m_array = [], b_array = [], m_std = 0.1, b_std = 0.1, tracktor_upper_limit = 10 ** 8, walker = 10):
        
        tracktor_upper_limit /= walker
        with concurrent.futures.ProcessPoolExecutor() as executor:

            results = [executor.submit(self.metropolis_hasting_list, m, b, m_array, b_array, m_std, b_std, int(tracktor_upper_limit)) for _ in range(walker)]

            final_m_array, final_b_array = [], []
            for f in concurrent.futures.as_completed(results):
                m_array, b_array = f.result()
                final_m_array = np.append(final_m_array, m_array)
                final_b_array = np.append(final_b_array, b_array)

        return final_m_array, final_b_array


    # metropolis-hasting, array way
    def metropolis_hasting_list(self, m, b, m_array = [], b_array = [], m_std = 0.1, b_std = 0.1, tracktor_upper_limit = 10 ** 8):

        for _ in tqdm(range(tracktor_upper_limit), desc="Processing items"):
            
            previous = self.possibility_of_data_given_model(m, b)
            
            # draw form distribution for interval
            # change the m and b 
            after_m = np.random.normal(m, m_std)
            after_b = np.random.normal(b, b_std)
            after = self.possibility_of_data_given_model(after_m, after_b)
            
            # acceptance prob
            acceptance_prob = np.min([1.0, after/previous])

            if np.random.rand() <= acceptance_prob:
                # if accept
                m = after_m
                b = after_b
                
            m_array.append(m)
            b_array.append(b)

        print("Metropolis fasting complete")
        return m_array, b_array

    # finding max in counts dict
    def find_max(self, counts):
        curr_max = 0
        position = []
        for key in counts.keys():
            frequency = counts[key]
            if frequency > curr_max:
                position = key
                curr_max = frequency
        return position, curr_max

    # work with list, show graph of index vs steps
    def index_data_plot(self, data1, data2):

        plt.figure()

        # Subplot 1 (top)
        plt.subplot(2, 1, 1)
        plt.plot(data1)
        # Adding labels to the axes
        plt.xlabel('Index')
        plt.ylabel('Data')
        # Adding a title to the plot
        plt.title('M')

        # Subplot 2 (bottom)
        plt.subplot(2, 1, 2)
        plt.plot(data2)
        plt.xlabel('Index')
        plt.ylabel('Data')
        plt.title('B')

        # Display the plot
        plt.show()

    def linear_model(self, x):
        
        return self.start_pointing[0]*x + self.start_pointing[1]

    def model_fit(self):
        # Plotting with error bars
        plt.errorbar(self.x, self.y, yerr=self.yerr, fmt='o', label='Data with Error Bars')
        x_fit = np.linspace(min(self.x), max(self.x), 100)
        y_fit = self.linear_model(x_fit)
        plt.plot(x_fit, y_fit, label='Fit', color='red')

        # Adding labels and title
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Plot with Error Bars')

        # Displaying legend
        plt.legend()

        # Display the plot
        plt.show()
        
    def main(self, tracktor_upper_limit = 10 ** 8):
        return self.metropolis_hasting_init(self.start_pointing[0], self.start_pointing[1], tracktor_upper_limit=tracktor_upper_limit)
        
if __name__ == "__main__":
    # for a spec issue that comes up 
    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    chain = MCMC()
    final_m_array, final_b_array = chain.main(tracktor_upper_limit = 10 ** 8)
    




        


