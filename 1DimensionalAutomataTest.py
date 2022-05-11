import numpy as np
import Utils
import time
import seaborn as sn
import sys
import random
from OneDimensionalCellularAutomaton import OneDimensionalCellularAutomaton

<<<<<<< HEAD

import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None
=======
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650
# print(int(np.base_repr(2730, base=16), 16))

# print(int("AAA", 16))

# print(np.base_repr(2730998, base=16))

# print(Utils.DIGITSETS)


<<<<<<< HEAD
base = 8
pop_size = 500
=======
base = 4
pop_size = 100
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650
def elementary_neighborhood(idx):
    if idx == 0:
        return [-1, 0, 1]
    elif idx == pop_size - 1:
        return [pop_size - 2, pop_size - 1, 0]
    else:
        return [idx - 3, idx, (idx + 3)%pop_size]

<<<<<<< HEAD
x = OneDimensionalCellularAutomaton(elementary_neighborhood, base=base, rule=int(random.randint(0, Utils.get_num_of_rules(5, base))), color_palette=sn.color_palette("BuPu_r", base),init_pop=[random.choice([str(x) if x < 10 else str(chr(55 + x)) for x in range(base)]) for i in range(pop_size)])
x.iterate(500)
=======
x = OneDimensionalCellularAutomaton(elementary_neighborhood, base=base, rule=int(random.randint(0, sys.maxsize)), color_palette=sn.color_palette("viridis", base),init_pop=[random.choice([str(x) if x < 10 else str(chr(55 + x)) for x in range(base)]) for i in range(pop_size)])
x.iterate(1000)
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650
x.generate_media(directory="images/1-D Automata/"+str(base)+"/")
print(x)
# print(Utils.get_transition_dictionary(5, 16, 512)['#rules'])