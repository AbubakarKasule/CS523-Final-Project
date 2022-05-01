"""
Author: Abubakar Kasule
Description: Utility functions for Cellular Automata 
Note: 
"""

# Imports
import numpy as np
import math
import random
# import networkx as nx

# Constants
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G"]
DIGITSETS = dict()

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



# Calculate Hamming Distance. 
def get_hamming_distance(bitstr1, bitstr2):
    count = 0

    n = len(bitstr1)
    m = len(bitstr2)

    if m != n:
        return math.inf # No hamming distance. String do not match


    for i in range(n):
        if bitstr1[i] != bitstr2[i]:
            count += 1

    return count



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