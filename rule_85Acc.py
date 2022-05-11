import numpy as np
import random
import matplotlib.pyplot as plt
from MultiDimensionalCellularAutomaton import MultiDimensionalCellularAutomaton

def perfect_memory_neighborhood(j):

    res = []

    for i in range(6):
        res.append(i)

    for i in range(6):
        res.append(i - j)

    return res


dimensions = (6,)
base = 2

# Target Function
def f(x):
    return x + 3

p= len(perfect_memory_neighborhood(0))

correct = 0
total = 0
pop_size = 6
results = []


print("Neighborhood found")
x = MultiDimensionalCellularAutomaton(perfect_memory_neighborhood, 
                                    neighborhood_size=p, 
                                    color_palette_idx=int(random.randint(0, 170)), #sn.color_palette("viridis", base), 
                                    base=base, 
                                    dimensions=dimensions, 
                                    rule=848637738250156742683518739735687334552097540160551227103550133341631541255058378719611970699960006487221740649979507286165159777196762954567221094675667417960943932809090159213803606880226172337122645658179860360141423498134465485736412021259871139801428859978822431452170113511767788149181532934622882608805936711821400674449777368313080103818521802489993542165205115614323644813577654343171344132703454490922809560164052704307234031318211362316148928057947711583683138409909849428530345187967220182631431112335498940154457734991151186688757595393995862298983313626756593852932613330080513044030429499811301299713850502044332661965353775329082183167915549958580839065489893286184014966913137205872269430117973693002755146127957791057774077387106999310188904310378486894472234204663242037454599633426563879055216106999206767424985113117755148223697817468403363516120126692753261721832615696179626096248124916577982147108455528959078426878742243454891001785175148659974836048474415908166099016342479798247805936017497614305993038879433525553440265930764295991584185477039537412105333293330787856981583219342209000208409175324719410622380601144124441575034677205613400890318723136163198312022684867340489577728557204242701346479943576,
                                    init_pop=['0', '1', '0', '1', '0', '1', '0', '1']) #generate_random_2d_pop(base, dimensions))


for n in range(60):
    # Reset
    input_list = list([i for i in str(np.base_repr(n, base=base)).rjust(pop_size, "0")])
    x.history = list([input_list])

    x.iterate(1, surpress_print=True)

    automata_answer = ""

    for j in x.return_latest_generation():
        automata_answer += j

    automata_answer = int(automata_answer, base)

    results.append(automata_answer)

    if f(n) == automata_answer:
        correct += 1


    total += 1


print("Accuracy: ", str(correct/total)[:4] + "%")



plt.plot(list(range(60)), results, label = "CA Model")
plt.plot(list(range(60)), [f(x) for x in range(60)], label = "Target Function")
plt.legend()
plt.savefig("Approximation graph 1")




