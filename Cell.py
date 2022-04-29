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


class Cell:
    def __init__(self, state, neighbors, base):
        self.state = state
        self.neighbors = neighbors
        self.base = base

    def get_next_state(self):
        digits = Utils.DIGITSETS[self.base]

        new_cell = Cell()
 



    def __str__(self):
        return "Cell: " + self.state