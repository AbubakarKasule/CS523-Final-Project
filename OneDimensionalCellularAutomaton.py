"""
Author: Abubakar Kasule
Description: Class used to represent Germinal Center
Note: Each GC starts with one epitope from the antigen. 
"""

# Imports
import functools
import Utils
import random
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sn


class OneDimensionalCellularAutomaton:
    def __init__(self, neighborhood_function, population_size=10, rule=30, init_pop=[0,0,1,0,0], base=2):
        self.rule = rule
        self.init_pop = init_pop
        self.base = base
        self.history = [init_pop]

    def apply_rule(self):
        res = list()

        curr = self.history[-1]



    def __str__(self):
        return "Rule:\n\n" + str(self.rule) + "\n\n" + "Base:\n\n" + str(self.base) + "\n\n" + "Result:\n\n" + str(self.history) + "\n\n" 