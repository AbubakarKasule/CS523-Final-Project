"""
Author: Abubakar Kasule
Description: Class used to represent different cellular automata configurations
Note: 
"""

# Imports
import functools
import Utils
import random
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sn
import numpy as np


class CellularAutomataConfig:

    ID = 1
    MUTATION_RATE = 0.1

    def __init__(self, rule, base, parent1=None, parent2=None, generation=0):
        self.id = CellularAutomataConfig.ID
        self.rule = rule
        self.base = base
        self.parents = (parent1, parent2)
        self.generation = generation

        CellularAutomataConfig.ID += 1

    # Run on children after creation
    def mutate(self):
        new_rule = ""

        for xit in self.rule:
            if random.random() < CellularAutomataConfig.MUTATION_RATE:
                new_rule += Utils.return_different_xit(xit, self.base)
            else:
                new_rule += xit

        self.rule = new_rule


    @staticmethod
    def create_random_config(base, dimensions, neighborhood_function):
        num_of_dimensions = len(dimensions)
        neighborhood_size = len(neighborhood_function(0))
        num_of_cell_states = base
        rule_length = num_of_cell_states**neighborhood_size
        rule = str(np.base_repr(random.randint(0, Utils.get_num_of_rules(neighborhood_size, base)), base=base)).rjust(rule_length, "0")
        
        # tuple([pop_size**(1/num_of_dimensions)] * num_of_dimensions)  # Balanced dimensions

        return CellularAutomataConfig(rule, base, num_of_dimensions, dimensions)

    @staticmethod
    def create_children_configs(parent1, parent2, generation):
        crossover_size = random.randint(0, len(parent1.rule) - 1)
        crossover_point = random.randint(0, len(parent1.rule) - crossover_size)

        donor_rule = parent1.rule[:crossover_point] + parent2.rule[crossover_point:crossover_point+crossover_size] + parent1.rule[crossover_point+crossover_size:]
        recipient_rule = parent2.rule[:crossover_point] + parent1.rule[crossover_point:crossover_point+crossover_size] + parent2.rule[crossover_point+crossover_size:]

        donor = CellularAutomataConfig(donor_rule, parent1.base, parent1=parent1, parent2=parent2, generation=generation)
        recipient = CellularAutomataConfig(recipient_rule, parent1.base, parent1=parent2, parent2=parent1, generation=generation)

        donor.mutate()
        recipient.mutate()

        return (donor, recipient)


    def __str__(self):
        return str(self.id) + "-" + str(self.generation)