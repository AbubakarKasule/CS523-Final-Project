import numpy as np
import Utils

# print(int(np.base_repr(2730, base=16), 16))

# print(int("AAA", 16))

# print(np.base_repr(2730998, base=16))

# print(Utils.DIGITSETS)

print(Utils.get_transition_dictionary(5, 16, 512)['#rules'])