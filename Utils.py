"""
Author: Abubakar Kasule
Description: Utility functions for Cellular Automata 
Note: 
"""

# Imports
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sn
import pandas as pd
# import networkx as nx

# Constants
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]
DIGITSETS = dict()
PALETTES = ["Accent", "Accent_r", "Blues", "Blues_r", "BrBG", "BrBG_r", "BuGn", "BuGn_r", "BuPu", "BuPu_r", 
 "CMRmap", "CMRmap_r", "Dark2", "Dark2_r", "GnBu", "GnBu_r", "Greens", "Greens_r", "Greys", "Greys_r", "OrRd", 
 "OrRd_r", "Oranges", "Oranges_r", "PRGn", "PRGn_r", "Paired", "Paired_r", "Pastel1", 
 "Pastel1_r", "Pastel2", "Pastel2_r", "PiYG", "PiYG_r", "PuBu", "PuBuGn", "PuBuGn_r", 
 "PuBu_r", "PuOr", "PuOr_r", "PuRd", "PuRd_r", "Purples", "Purples_r", "RdBu", "RdBu_r", 
 "RdGy", "RdGy_r", "RdPu", "RdPu_r", "RdYlBu", "RdYlBu_r", "RdYlGn", "RdYlGn_r", "Reds", 
 "Reds_r", "Set1", "Set1_r", "Set2", "Set2_r", "Set3", "Set3_r", "Spectral", "Spectral_r", 
 "Wistia", "Wistia_r", "YlGn", "YlGnBu", "YlGnBu_r", "YlGn_r", "YlOrBr", "YlOrBr_r", "YlOrRd", 
 "YlOrRd_r", "afmhot", "afmhot_r", "autumn", "autumn_r", "binary", "binary_r", "bone", 
 "bone_r", "brg", "brg_r", "bwr", "bwr_r", "cividis", "cividis_r", "cool", "cool_r", "coolwarm", "coolwarm_r", "copper", "copper_r",
 "cubehelix", "cubehelix_r", "flag", "flag_r", "gist_earth", "gist_earth_r", "gist_gray", "gist_gray_r", "gist_heat", "gist_heat_r", "gist_ncar", "gist_ncar_r",
 "gist_rainbow", "gist_rainbow_r", "gist_stern", "gist_stern_r", "gist_yarg", 
 "gist_yarg_r", "gnuplot", "gnuplot2", "gnuplot2_r", "gnuplot_r", "gray", "gray_r",
 "hot", "hot_r", "hsv", "hsv_r", "icefire", "icefire_r", "inferno", 
 "inferno_r", "magma", "magma_r", "mako", "mako_r", 
 "nipy_spectral", "nipy_spectral_r", "ocean", "ocean_r", "pink", "pink_r",
 "plasma", "plasma_r", "prism", "prism_r", "rainbow", "rainbow_r",
 "rocket", "rocket_r", "seismic", "seismic_r", "spring", "spring_r",
 "summer", "summer_r", "tab10", "tab10_r", "tab20", "tab20_r", "tab20b",
 "tab20b_r", "tab20c", "tab20c_r", "terrain", "terrain_r", "twilight",
 "twilight_r", "twilight_shifted", "twilight_shifted_r", "viridis", "viridis_r", "vlag", "vlag_r", "winter", "winter_r"]
 
for i in range(2, 17):
    DIGITSETS[i] = list(DIGITS[0 : i])

# Functions
def get_new_state(neighborhood, curr_state, rule, base):
    pass

"""
a: # cells in nbhd
b: possible # of cell states
c: b^a length of each rule
# of rules: b^c

Function to map neighborhood to new state
"""
def get_transition_dictionary(neighborhood_size, base, rule):
    res = dict()
    num_of_cell_states = len(DIGITSETS[base])
    rule_length = num_of_cell_states**neighborhood_size
    num_of_rules = num_of_cell_states**rule_length

    rule_string = str(np.base_repr(rule, base=base)).rjust(rule_length, "0")

    for i in range(rule_length):
        res[str(np.base_repr(i, base=base)).rjust(neighborhood_size, "0")] = rule_string[-1 - i]

    res['rule'] = rule_string
    # res['#rules'] = num_of_rules

    return res

def get_num_of_rules(neighborhood_size, base):
    num_of_cell_states = len(DIGITSETS[base])
    rule_length = num_of_cell_states**neighborhood_size
    num_of_rules = num_of_cell_states**rule_length

    return num_of_rules
<<<<<<< HEAD

def apply_rule_parallel(input_tuple):
    self, target_function, n = input_tuple
    res = list()
    curr = list([i for i in str(np.base_repr(n, base=self.base)).rjust(self.base**self.neighborhood_size, "0")])

    for i in range(len(curr)):

        try:
            nbrs = self.get_neighbors(i)
            nbrs_string = ""

            for j in nbrs:
                nbrs_string += curr[j]

            res.append(self.transition_dictionary[nbrs_string])
        except:
            print(nbrs, "o", curr)
=======
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650

    temp = ""

    for c in res:
        temp += c

    if int(temp, self.base) == target_function(n):
        return 1
    else:
        return 0

def produce_image_parallel(i):
    directory, n, legend, annot, history, dimensions, color_palette_idx, base = i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]
    res = list()

    for i in range(dimensions[0]):
        temp = list()

        for j in range(dimensions[1]):
            temp.append(int(history[n][(i * dimensions[1]) + j], base=base))

        res.append(temp)

    df_cm = pd.DataFrame(res)
    plt.figure(figsize = (dimensions[1], dimensions[0])) #(20,20)
    sn.heatmap(df_cm, annot=annot, cbar=legend, cmap=sn.color_palette(PALETTES[color_palette_idx], base))  # sn.color_palette("viridis", base)

    if legend:
        plt.xlabel("Cell Number")
        plt.ylabel("Generation")
    
    plt.axis('off')

    plt.savefig(directory + str(n), bbox_inches='tight')
    plt.clf()
    plt.close('all')


"""
id|base|#dimensions|dimensions|neighborhood_function_idx|rule|neighborhood_size
"""

def create_cellular_automata_dna(id, parent1, parent2):
    pass

def return_different_xit(xit, base):
    l = list(DIGITSETS[base])
    l.remove(xit)

    return random.choice(l)

# Copied from https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments
        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed
        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)