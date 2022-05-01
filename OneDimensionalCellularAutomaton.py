"""
Author: Abubakar Kasule
Description: Class used to represent a one dimensional CA
Note:  
"""

# Imports
import functools
import Utils
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sn
import numpy as np
import sys
import time


class OneDimensionalCellularAutomaton:
    def __init__(self, neighborhood_function, neighborhood_size=3, population_size=10, rule=30, init_pop=['0','0','1','0','0'], base=2):
        self.rule = rule
        self.init_pop = init_pop
        self.base = base
        self.history = [init_pop]
        self.get_neighbors = neighborhood_function
        self.neighborhood_size = neighborhood_size
        self.transition_dictionary = Utils.get_transition_dictionary(neighborhood_size, base, rule)

    def apply_rule(self):
        res = list()
        curr = self.history[-1]
        

        for i in range(len(curr)):
            nbrs = self.get_neighbors(i)
            nbrs_string = ""

            for j in nbrs:
                nbrs_string += curr[j]

            res.append(self.transition_dictionary[nbrs_string])

        self.history.append(res)

    def return_latest_generation(self):
        return self.history[-1]      

    def iterate(self, x):
        # print(len(self.transition_dictionary.keys()))
        ERASE_LINE = '\x1b[2K'
        
        print("\nIteration Progress:\n")
        for i in range(x):
            
            self.apply_rule()
            b = "[" + str("X" * i) + str("-" * (x - (i + 1))) + "]"
            sys.stdout.write(ERASE_LINE+'\r')
            print(b, end="")
            # time.sleep(0.1)
            
        print("\n")

    def get_base_n_input(self, n):
        res = "" 

        for c in self.history[0]:
            res += c

        return np.base_repr(int(res, self.base), base=n)

    def get_base_n_output(self, n):
        res = "" 

        for c in self.history[-1]:
            res += c

        return np.base_repr(int(res, self.base), base=n)

    def get_base_n_intermediate_output(self, n, i):
        res = "" 

        for c in self.history[i]:
            res += c

        return np.base_repr(int(res, self.base), base=n)

    def get_population_size(self):
        return len(self.history[0])

    def get_rule(self):
        return self.rule

    def get_base(self):
        return self.base

    def generate_media(self, legend=False, annot=False, directory="./"):
        array = list()

        for gen in self.history:
            array.append(list([int(x, base=self.base) for x in gen]))

        df_cm = pd.DataFrame(array, index =list([x for x in range(len(self.history))]), columns =list([x for x in range(len(self.history[0]))]))
        plt.figure(figsize = (20,20)) 
        sn.heatmap(df_cm, annot=annot, cbar=legend)

        if legend:
            plt.xlabel("Cell Number")
            plt.ylabel("Generation")
        else:
            plt.axis('off')

        plt.savefig(directory + str(self.get_base())+ "-" + str(self.get_rule())+ "-" + str(self.get_population_size()), bbox_inches='tight')

    def __str__(self):
        first = ""  
        last = ""

        for c in self.history[0]:
            first += c

        for c in self.history[-1]:
            last += c

        first_10 = int(first, self.base)
        last_10 = int(last, self.base)

        return "CA Details:\n\n - Rule: " + \
            str(self.rule) + "\n - Base: " + str(self.base) + \
            "\n - Neighborhood Size: " + str(self.neighborhood_size) + \
            "\n - Number of Iterations: " + str(len(self.history) - 1) + \
            "\n - Population Size: " + str(len(self.history[0])) + "\n\n" + \
            "Inputs:\n\n - Base_" + str(self.base) + ": " + first + "\n - Base_10: " + str(first_10) + \
            "\n\nOutputs:\n\n - Base_" + str(self.base) + ": " + last + "\n - Base_10: " + str(last_10) + \
            "\n\n------------DONE------------\n"
