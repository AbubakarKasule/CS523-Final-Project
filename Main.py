"""
Author: Abubakar Kasule
Description: Driver code for my genetic algorithm
Note:
"""
# Imports
from CAGA import CellularAutomataGeneticAlgorithm
from CellularAutomataConfig import CellularAutomataConfig
import matplotlib.pyplot as plt
import os
import random
import platform
from colorama import Fore, Style, init
import math
import os
import sys
import multiprocessing as mp
from multiprocessing import Pool

init(autoreset=True)

# Constants
NUMBER_OF_GENETIC_ALGORITHMS = 1
CELLULAR_AUTOMATA_POPULATION_SIZE = 4
RULE_MUTATION_RATE = 0.005 #0.005  # very sensitive to mutation rate
NUMBER_OF_GENERATIONS = 100


dimensions = (8,)
base = 2

# Target Function
def f(x):
    return x**2

# Neighborhood functions
def game_of_life_neighborhood(idx):
    def get_idx(r, c):
        _r = r
        _c = c

        if _r < 0:
            _r = dimensions[0] - 1
        elif _r >= dimensions[0]:
            _r = 0

        if _c < 0:
            _c = dimensions[1] - 1
        elif _c >= dimensions[1]:
            _c = 0

        
        return (_r * dimensions[1]) + _c

    row = -1
    temp = 0

    while temp <= idx:
        row += 1
        temp += dimensions[1]

    col = idx - (row * dimensions[1])

    """
    [get_idx(row - 1, col - 1), get_idx(row - 1, col), get_idx(row - 1, col + 1),
            get_idx(row, col - 1), get_idx(row, col), get_idx(row, col + 1),
            get_idx(row + 1, col - 1), get_idx(row + 1, col), get_idx(row + 1, col + 1)]
    
    [get_idx(row - 1, col - 1), get_idx(row - 1, col + 1),
            get_idx(row, col),
            get_idx(row + 1, col - 1), get_idx(row + 1, col + 1)]
    
    [get_idx(row - 2, col - 2), get_idx(row - 2, col + 2),
            get_idx(row - 1, col - 1),
            get_idx(row - 1, col + 1), 
            get_idx(row, col),
            get_idx(row + 1, col), get_idx(row + 2, col), get_idx(row + 3, col)]
    """

    # tl, tc, tr - ml, [mc], mr - bl, bc, br
    return [get_idx(row - 1, col - 1), get_idx(row - 1, col), get_idx(row - 1, col + 1),
            get_idx(row, col - 1), get_idx(row, col), get_idx(row, col + 1),
            get_idx(row + 1, col - 1), get_idx(row + 1, col), get_idx(row + 1, col + 1)]

def game_of_life_neighborhood_alt(idx):
    def get_idx(r, c):
        _r = r
        _c = c

        if _r < 0:
            _r = dimensions[0] - 1
        elif _r >= dimensions[0]:
            _r = 0

        if _c < 0:
            _c = dimensions[1] - 1
        elif _c >= dimensions[1]:
            _c = 0

        
        return (_r * dimensions[1]) + _c

    row = -1
    temp = 0

    while temp <= idx:
        row += 1
        temp += dimensions[1]

    col = idx - (row * dimensions[1])

    """
    [get_idx(row - 1, col - 1), get_idx(row - 1, col), get_idx(row - 1, col + 1),
            get_idx(row, col - 1), get_idx(row, col), get_idx(row, col + 1),
            get_idx(row + 1, col - 1), get_idx(row + 1, col), get_idx(row + 1, col + 1)]
    
    [get_idx(row - 1, col - 1), get_idx(row - 1, col + 1),
            get_idx(row, col),
            get_idx(row + 1, col - 1), get_idx(row + 1, col + 1)]
    
    [get_idx(row - 2, col - 2), get_idx(row - 2, col + 2),
            get_idx(row - 1, col - 1),
            get_idx(row - 1, col + 1), 
            get_idx(row, col),
            get_idx(row + 1, col), get_idx(row + 2, col), get_idx(row + 3, col)]
    """

    # tl, tc, tr - ml, [mc], mr - bl, bc, br
    return [get_idx(row - 1, col - 1), get_idx(row - 1, col + 1),
            get_idx(row, col),
            get_idx(row + 1, col - 1), get_idx(row + 1, col + 1)]

def perfect_memory_neighborhood(j):

    res = []

    for i in range(8):
        res.append(i)

    for i in range(8):
        res.append(i - j)

    # while len(res) < 16:
    #     res.append(j)

    return res
    # idx = 1
    # return [j, idx - 1, idx - 2, idx - 3, idx - 4, idx - 5, idx - 6, idx - 7, idx - 8]


def row_check_neighborhood(idx):
    def get_idx(r, c):
        _r = r
        _c = c

        if _r < 0:
            _r = dimensions[0] - 1
        elif _r >= dimensions[0]:
            _r = 0

        if _c < 0:
            _c = dimensions[1] - 1
        elif _c >= dimensions[1]:
            _c = 0

        
        return (_r * dimensions[1]) + _c

    row = -1
    temp = 0

    while temp <= idx:
        row += 1
        temp += dimensions[1]

    col = idx - (row * dimensions[1])

    """
    [get_idx(row - 1, col - 1), get_idx(row - 1, col), get_idx(row - 1, col + 1),
            get_idx(row, col - 1), get_idx(row, col), get_idx(row, col + 1),
            get_idx(row + 1, col - 1), get_idx(row + 1, col), get_idx(row + 1, col + 1)]
    
    [get_idx(row - 1, col - 1), get_idx(row - 1, col + 1),
            get_idx(row, col),
            get_idx(row + 1, col - 1), get_idx(row + 1, col + 1)]
    
    [get_idx(row - 2, col - 2), get_idx(row - 2, col + 2),
            get_idx(row - 1, col - 1),
            get_idx(row - 1, col + 1), 
            get_idx(row, col),
            get_idx(row + 1, col), get_idx(row + 2, col), get_idx(row + 3, col)]
    """

    # tl, tc, tr - ml, [mc], mr - bl, bc, br
    return [get_idx(row - 1, col - 1), get_idx(row - 1, col), get_idx(row - 1, col + 1),
            get_idx(row, col)]


# variables
genetic_algorithms = []
neighborhood_functions = [(game_of_life_neighborhood, dimensions), (row_check_neighborhood, dimensions), (perfect_memory_neighborhood, dimensions)]

# Initialize CAGAs
for i in range(NUMBER_OF_GENETIC_ALGORITHMS):
    _x = neighborhood_functions[2]
    genetic_algorithms.append(CellularAutomataGeneticAlgorithm(CELLULAR_AUTOMATA_POPULATION_SIZE, _x[1], f, 1, _x[0], base, mutation_rate=RULE_MUTATION_RATE, testing_range=(0, 16)))

# Initialize ca populations
for ga in genetic_algorithms:
    
    ga.initialize_cellular_automata_population()

    # 44.4%
    # ga.add_rule_to_pop(455670610578522246272080939337516358843198623212875982982743515102054057026553032781950518633740019964700982286936165564944224796241560337894014304857314224959149751592099987519683486697027207277168298369460054831755521018543632249166173258822820825413255210629222892923674283536367820515691409404750945105343881547561807602321644949158605603452614007174290823943017660000331746042669060635522682093261425628161599794355748846769941015169086765182846447121979981040534550589962156258579680699997879550050349312322317450160576531564090955064756266515818587404641255262010065491355627012943138612422888697423244054544307182343309279490214828848619840180671923955535119815509589186373912218066923922195937423284112539968150630379602641883194379180640609135721591569029852335953941407220105667976272476929290274494306874603003409996009880512944421816130225844013815844692431016931894442592892636981429921959395231259953854979867710010548523956384980869796591456173654516461920633630856081679969841290310981197508373968347147078711448833007608873063977086577516323365279717052438207128840320600246590322263198463481354769142512893220293953587385584825370285345828194288683031182268096599361809936266271331854594554501806947400349048605220)
    

# Simulate evolution

print(0)

increase_1 = True
increase_2 = True
prev_acc = 0

mutation_rates = iter([0.0005, 0.0008, 0.0001])

prev_acc = 0
_rate = RULE_MUTATION_RATE

def run(num__):
    global increase_1, increase_2, prev_acc, _rate
    
    emotesv = ["▚", "▞"] #["⇋", " ", "⇌", " "]
    h =  ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"] #["-", "\\", "|", "/"]
    ERASE_LINE = '\x1b[2K'
    block_size = 40/NUMBER_OF_GENERATIONS
    x = NUMBER_OF_GENERATIONS
    for ga in genetic_algorithms:
        print("\nIteration Progress: " + str(num__), end="\n")
        curr_generation = 1
        while (curr_generation <= NUMBER_OF_GENERATIONS):
            CellularAutomataConfig.ID = 21  # reset id count for each ga
            ga.selection_and_reproduction()

            i = curr_generation - 1

            offset = math.ceil(block_size * i)
            _offset = 40 - offset
            b = " |" + str("█") * offset + str(emotesv[i%2]) * (_offset) + "| " +  h[i%8] + " " + str((i + 1)/x * 100)[:5] + "% Complete..."

            c = Fore.GREEN

            if platform.system().lower() == 'windows':
                sys.stdout.write(ERASE_LINE+'\r')
                print(c + b, end="")
            else:
                print(c + b, end="\r")

            curr_generation += 1

        acc = ga.get_fitness(ga.return_best_automata())

        print("\nAccuracy: ", str(acc * 100)[:4]+"%")

        if prev_acc == acc:
            print("\nMutation rate boosted")
            _rate = _rate / 2

            if _rate > 1:
                _rate = 1
            ga.set_mutation_rate(_rate)

            # Double population
            for __item in range(len(ga.automata_population)):
                # if __item == 0:
                #     ga.add_rule_to_pop(455670610578522246272080939337516358843198623212875982982743515102054057026553032781950518633740019964700982286936165564944224796241560337894014304857314224959149751592099987519683486697027207277168298369460054831755521018543632249166173258822820825413255210629222892923674283536367820515691409404750945105343881547561807602321644949158605603452614007174290823943017660000331746042669060635522682093261425628161599794355748846769941015169086765182846447121979981040534550589962156258579680699997879550050349312322317450160576531564090955064756266515818587404641255262010065491355627012943138612422888697423244054544307182343309279490214828848619840180671923955535119815509589186373912218066923922195937423284112539968150630379602641883194379180640609135721591569029852335953941407220105667976272476929290274494306874603003409996009880512944421816130225844013815844692431016931894442592892636981429921959395231259953854979867710010548523956384980869796591456173654516461920633630856081679969841290310981197508373968347147078711448833007608873063977086577516323365279717052438207128840320600246590322263198463481354769142512893220293953587385584825370285345828194288683031182268096599361809936266271331854594554501806947400349048605220)
                # else:
                ga.add_random_rule_to_pop()

        else:
            prev_acc = acc


        # if acc > 0.7 and increase_1:
        #     ga.set_mutation_rate(0.01)
        #     increase_1 = False
        # elif acc > 0.9 and increase_2:
        #     ga.set_mutation_rate(0.05)
        #     increase_2 = False


p__ = 1
while genetic_algorithms[0].get_fitness(genetic_algorithms[0].return_best_automata()) < 0.75:
    run(p__)
    p__ += 1

"""
def func(ga):
    curr_generation = 1
    while (curr_generation <= 1000):
         
        ga.selection_and_reproduction()

        curr_generation += 1

with Pool(NUMBER_OF_GENETIC_ALGORITHMS) as p:
    p.map(func, genetic_algorithms)
"""
print(1)

with open('results.txt', 'w') as f:
    for i in range(len(genetic_algorithms)):
        ga = genetic_algorithms[i]
        print("Genetic Algorithm #" + str(i + 1) + ": ", end="", file=f)
        print("From: " + str(ga.performance_history[0]), "To: " + str(ga.performance_history[-1]), "Rule: " + str(int(ga.return_best_automata().rule, base)), "Dimensions: " + str(ga.dimensions), file=f)


# Graphics stuff

# line graph fitness x generation for each ga
for i in range(len(genetic_algorithms)):
    ga = genetic_algorithms[i]
    ga.generate_fitness_to_generation_graph("generation_fitness_graphs/ga" + str(i + 1))

# lineage of best antibody demarcated by generation
for i in range(len(genetic_algorithms)):
    ga = genetic_algorithms[i]
    ga.generate_lineage_tree_for_best_rule("lineage_trees/ga" + str(i + 1), 10)


# bar graph comparing ga success

ga_ids = ["ga#" + str(x + 1) for x in range(NUMBER_OF_GENETIC_ALGORITHMS)]
ga_best_fitness = [x.get_fitness(x.return_best_automata()) * 100 for x in genetic_algorithms]
plt.figure(3,figsize=(15, 10))
plt.bar(ga_ids, ga_best_fitness)

plt.xlabel("Genetic Algorithm")
plt.ylabel("Fitness")
plt.title("Fitness Comparison between Genetic Algorithms")
plt.savefig("ga results")
plt.clf()


print("End of Code")
