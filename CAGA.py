"""
Author: Abubakar Kasule
Description: Genetic algorithm for finding Cellular Automata rules that approximate a given function
Note:  
"""

# Imports
import functools
import Utils
import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import multiprocessing as mp
from multiprocessing import Pool
from CellularAutomataConfig import CellularAutomataConfig
from MultiDimensionalCellularAutomaton import MultiDimensionalCellularAutomaton
#from networkx.drawing.nx_agraph import graphviz_layout

class CellularAutomataGeneticAlgorithm:
    def __init__(self, population_size, dimensions, target_function, itr_num, neighborhood_function, base, threads=-1, testing_range=(0, 99), mutation_rate=None):
        self.population_size = population_size
        self.automata_population = []   # Empty until population is initialized
        self.generation = 1
        self.performance_history = []
        self.testing_range = testing_range
        self.target_function = target_function
        self.base = base
        self.neighborhood_function = neighborhood_function
        self.dimensions = dimensions
        self.itr_num = itr_num
        self.threads = threads

        if mutation_rate is not None:
            CellularAutomataConfig.MUTATION_RATE = mutation_rate

    def set_mutation_rate(self, mutation_rate):
        CellularAutomataConfig.MUTATION_RATE = mutation_rate

    def initialize_cellular_automata_population(self):
        for i in range(self.population_size):
            self.automata_population.append(CellularAutomataConfig.create_random_config(self.base, self.dimensions, self.neighborhood_function))

    def add_rule_to_pop(self, rule_int):
        num_of_dimensions = len(self.dimensions)
        neighborhood_size = len(self.neighborhood_function(0))
        num_of_cell_states = self.base
        rule_length = num_of_cell_states**neighborhood_size
        rule = str(np.base_repr(rule_int, base=self.base)).rjust(rule_length, "0")

        self.automata_population.append(CellularAutomataConfig(rule, self.base, num_of_dimensions, self.dimensions))
        self.population_size = self.population_size + 1

    def add_random_rule_to_pop(self):
        self.automata_population.append(CellularAutomataConfig.create_random_config(self.base, self.dimensions, self.neighborhood_function))
        self.population_size = self.population_size + 1

    def get_fitness(self, automata, transition_fitness=False):

        pop_size = 1

        for i in self.dimensions:
            pop_size = pop_size * i

        x = MultiDimensionalCellularAutomaton(self.neighborhood_function, 
                                            neighborhood_size=len(self.neighborhood_function(0)), 
                                            color_palette_idx=int(random.randint(0, 170)),
                                            base=self.base, 
                                            dimensions=self.dimensions, 
                                            rule=int(automata.rule, self.base),
                                            init_pop=[])

        if self.threads < 1:
        
            correct = 0
            total = 0
            
            for n in range(self.testing_range[0], self.testing_range[1]):
                # Reset
                input_list = list([i for i in str(np.base_repr(n, base=self.base)).rjust(pop_size, "0")])
                x.history = list([input_list])
                
                # Calculate
                x.iterate(self.itr_num, surpress_print=True)

                # Evaluate

                if transition_fitness:
                    true_answer = list(str(np.base_repr(self.target_function(n), base=self.base)).rjust(pop_size, "0"))
                    # print(true_answer)
                    partial_matches = 0
                    for idx in range(pop_size):
                        if x.return_latest_generation()[idx] == true_answer[idx]:
                            partial_matches += 1

                    if partial_matches == pop_size:
                        correct += pop_size//2  # Bias for being all correct

                    correct += partial_matches
                    total += pop_size
                        
                else:
                    automata_answer = ""

                    for j in x.return_latest_generation():
                        automata_answer += j

                    automata_answer = int(automata_answer, self.base)

                    if self.target_function(n) == automata_answer:
                        correct += 1

                    total += 1
                
            return correct / total
        
        else:
            with Pool(self.threads) as p:
                parallel_output = p.map(Utils.apply_rule_parallel, [(x, self.target_function, test_value) for test_value in range(self.testing_range[0], self.testing_range[1])])

            return sum(parallel_output) / len(parallel_output)

    def get_fitness_mse(self, automata):
        pass

    def fitness_comparator(self, item1, item2):
        _1 = self.get_fitness(item1, transition_fitness=True)
        _2 = self.get_fitness(item2, transition_fitness=True)
        if _1 < _2:
            return -1
        elif _1 > _2:
            return 1
        else:
            return 0

    def selection_and_reproduction(self):
        # print(0, end='')
        
        # Sort by fitness
        self.automata_population = sorted(self.automata_population, key=functools.cmp_to_key(self.fitness_comparator))

        # get rid of low performing Antibodies. Shuffle the ant
        self.automata_population = list(self.automata_population[len(self.automata_population)//2:])
        random.shuffle(self.automata_population)

        # create new final population by breeding remaining
        n = len(self.automata_population) - 1
        
        for i in range(0, n, 2):
            children = CellularAutomataConfig.create_children_configs(self.automata_population[i], self.automata_population[i + 1], self.generation)
            self.automata_population.append(children[0])
            self.automata_population.append(children[1])


        if (len(self.automata_population) != self.population_size):
            print("SOMETHING IS VERY WRONG: CAGA")

        for au in  range(len(self.automata_population)): 
            if self.get_fitness(self.automata_population[au]) < 0.001:
                self.automata_population[au] = CellularAutomataConfig.create_random_config(self.base, self.dimensions, self.neighborhood_function)
            
        self.generation += 1
    
        # Record fitness of best antibody
        self.performance_history.append(self.get_fitness(self.return_best_automata()))



    def return_best_automata(self):
        # Sort by fitness
        self.automata_population = sorted(self.automata_population, key=functools.cmp_to_key(self.fitness_comparator))
        with open('pop.txt', 'w') as f:
            print([self.get_fitness(x) for x in self.automata_population], file=f)

        return self.automata_population[-1]

    # Graphics functions
    def generate_fitness_to_generation_graph(self, filename):
        gens = [int(x + 1) for x in range(len(self.performance_history))]

        plt.xlabel("Generation")
        plt.ylabel("Fitness")
        plt.title("Fitness Comparison between Generations")
        #plt.xticks(gens, gens[::2])

        plt.gca().xaxis.set_major_locator(plt.MultipleLocator(100))

        plt.plot(gens, self.performance_history)
        plt.savefig(filename)
        plt.clf()

    def generate_lineage_tree_for_best_rule(self, filename, max_nodes):
        g = nx.DiGraph()

        nodes = [self.return_best_automata()]

        #print(nodes, "o000")

        curr = 0

        # Add nodes until out of range error
        try:
            while True and len(nodes) < max_nodes:
                parents = nodes[curr].parents

                if parents[0] is not None and parents[1] is not None:
                    if parents[0] not in nodes:
                        nodes.append(parents[0])

                    if parents[1] not in nodes:
                        nodes.append(parents[1])

                curr += 1
        except:
            print("No more nodes to add")

        # Add nodes to graph/tree
        for node in nodes:
            if (type(node) != type(self.return_best_automata())):
                continue
            parents = node.parents
            
            for prnt in list(parents):
                if prnt is not None:
                    if str(str(prnt) + "\n") in g:
                        i = 1

                        while str(str(prnt) + "-" + str(i) + "\n") in g:
                            i += 1

                        g.add_edge(str(node) + "\n", str(str(prnt) + "-" + str(i) + "\n"))
                    
                    else:
                        g.add_edge(str(node) + "\n", str(prnt) + "\n")

        if (len(nodes) == 0):
            print("yyyyy")

        plt.figure(3,figsize=(12, 5))
        plt.title("Lineage tree for best performing Automata Config")

        pos=Utils.hierarchy_pos(g, str(nodes[0]) + "\n", 100)
        nx.draw(g, pos=pos, node_size=50, with_labels=True, arrows=False)

        
        plt.savefig(filename)
        plt.clf()