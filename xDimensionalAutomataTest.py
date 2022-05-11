import numpy as np
import Utils
import math
import seaborn as sn
import sys
import random
from MultiDimensionalCellularAutomaton import MultiDimensionalCellularAutomaton

<<<<<<< HEAD
"""
# Uncomment when dealing with the creation of BIG images

import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000
"""
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000

base = 2
pop_size = 8 #500**2
dimensions= tuple([pop_size])#(int(math.sqrt(pop_size)), int(math.sqrt(pop_size)))
=======
# print(int(np.base_repr(2730, base=16), 16))

# print(int("AAA", 16))

# print(np.base_repr(2730998, base=16))

# print(Utils.DIGITSETS)


base = 3
pop_size = 100**2
dimensions= (int(math.sqrt(pop_size)), int(math.sqrt(pop_size)))
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650

def generate_random_2d_pop(base, dimensions):
    # [ for i in range(pop_size)]
    res = list()

    t = [str(x) if x < 10 else str(chr(55 + x)) for x in range(base)]

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            res.append(random.choice(t))

    return res

<<<<<<< HEAD
=======

>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650
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
<<<<<<< HEAD
    
    [get_idx(row - 2, col - 2), get_idx(row - 2, col + 2),
            get_idx(row - 1, col - 1),
            get_idx(row - 1, col + 1), 
            get_idx(row, col),
            get_idx(row + 1, col), get_idx(row + 2, col), get_idx(row + 3, col)]
    """

    # tl, tc, tr - ml, [mc], mr - bl, bc, br
    return [get_idx(row - 1, col - 1), get_idx(row, col), get_idx(row + 1, col + 1), get_idx(row + 2, col + 2)]


def elementary_neighborhood(idx):
    if idx == 0:
        return [-1, 0, 1]
    elif idx == pop_size - 1:
        return [pop_size - 2, pop_size - 1, 0]
    else:
        return [idx - 1, idx, idx + 1]

p= 3 #len(game_of_life_neighborhood(0))

print("Neighborhood found")
x = MultiDimensionalCellularAutomaton(elementary_neighborhood, 
                                    neighborhood_size=p, 
                                    color_palette_idx=int(random.randint(0, 170)), #sn.color_palette("viridis", base), 
                                    base=base, 
                                    dimensions=dimensions, 
                                    rule=170, #int(random.randint(0, Utils.get_num_of_rules(p, base))), 
                                    init_pop=['0', '1', '0', '1', '0', '1', '0', '1']) #generate_random_2d_pop(base, dimensions))
                                    
x.iterate(1)
#x.generate_media(directory="videos/"+str(base)+"/", threads=75)
print(x)

"""
print("Neighborhood found")
x = MultiDimensionalCellularAutomaton(game_of_life_neighborhood, 
                                    neighborhood_size=p, 
                                    color_palette_idx=int(random.randint(0, 170)), #sn.color_palette("viridis", base), 
                                    base=base, 
                                    dimensions=dimensions, 
                                    rule=int(random.randint(0, Utils.get_num_of_rules(p, base))), 
                                    init_pop=generate_random_2d_pop(base, dimensions))
                                    
x.iterate(80)
x.generate_media(directory="videos/"+str(base)+"/", threads=75)
print(x)
"""
=======
    """

    # tl, tc, tr - ml, [mc], mr - bl, bc, br
    return [get_idx(row - 1, col - 1), get_idx(row - 1, col + 1),
            get_idx(row, col),
            get_idx(row + 1, col - 1), get_idx(row + 1, col + 1)]

x = MultiDimensionalCellularAutomaton(game_of_life_neighborhood, 
                                    neighborhood_size=len(game_of_life_neighborhood(0)), 
                                    color_palette=sn.color_palette("viridis", base), 
                                    base=base, 
                                    dimensions=dimensions, 
                                    rule=int(random.randint(0, Utils.get_num_of_rules(5, base))), 
                                    init_pop=generate_random_2d_pop(base, dimensions))
                                    
x.iterate(1000)
x.generate_media(directory="videos/"+str(base)+"/")
print(x)
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650
