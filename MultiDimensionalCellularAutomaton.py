"""
Author: Abubakar Kasule
Description: Class used to represent an X dimensional CA
Note: Dimensions above 1 still nee to be represented by a single array

    For Example:
                       [[1, 5, 3],
        The 2D-Array    [6, 9, 9],  should be represented as the 1D-Array [1, 5, 3, 6, 9, 9, 3, 2, 5]
                        [3, 2, 5]] 

    Your Neighborhood function should account for this when returning the indeces of the neighbors

    A tuple describing the shape of your data must also be included

    For Example:

       [[[5, 7, 7], [8, 1, 3], [6, 5, 6]],
        [[1, 1, 0], [9, 9, 7], [3, 3, 1]]]   --->   (2, 3, 3) ---> [5, 7, 7, 8, 1, 3, 6, 5, 6, 1, 1, 0, 9, 9, 7, 3, 3, 1, 4, 7, 3, 9, 0, 4, 7, 7, 4]

    This is required for your data to be interpreted properly
"""

# Imports
import functools
import Utils
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sn
import numpy as np
import sys
import math
import os
import time
import moviepy.video.io.ImageSequenceClip

class MultiDimensionalCellularAutomaton:
    def __init__(self, neighborhood_function, neighborhood_size=3, rule=30, dimensions=(3, 3), init_pop=['0', '0', '1', '0', '1', '1', '0', '0', '1'], base=2, color_palette=None):
        self.rule = rule
        self.base = base
        self.history = [init_pop]
        self.dimensions = dimensions
        self.get_neighbors = neighborhood_function
        self.neighborhood_size = neighborhood_size
        self.color_palette = color_palette
        self.transition_dictionary = Utils.get_transition_dictionary(neighborhood_size, base, rule)

    def apply_rule(self):
        res = list()
        curr = self.history[-1]

        for i in range(len(curr)):
            nbrs = self.get_neighbors(i)
            nbrs_string = ""

            for j in nbrs:
                nbrs_string += curr[j]

            res.append(self.transition_dictionary[nbrs_string])

        self.history.append(res)

    def return_latest_generation(self):
        return self.history[-1]      

    def iterate(self, x):
        ERASE_LINE = '\x1b[2K'
        
        print("\nIteration Progress:\n")
        emotesv = ["<", "<", ">"]
        h = ["-", "\\", "|", "/"]

        block_size = 50/x

        for i in range(x):
            
            self.apply_rule()
            offset = math.ceil((i + 1) * block_size)       # 
            _offset = math.floor((block_size * (x - i - 1)) / 2)
            b = "[" + str("=" * offset) + str(emotesv[i%3] + emotesv[(i + 1)%3] + emotesv[(i + 2)%3]) * _offset + "]  " +  h[i%4] + " " + str((i + 1)/x * 100)[:4] + "% Complete..."
            sys.stdout.write(ERASE_LINE+'\r')
            print(b, end="")
            time.sleep(0.05)
            
        print("\n")

    def get_base_n_input(self, n):
        res = "" 

        for c in self.history[0]:
            res += c

        return np.base_repr(int(res, self.base), base=n)

    def get_base_n_output(self, n):
        res = "" 

        for c in self.history[-1]:
            res += c

        return np.base_repr(int(res, self.base), base=n)

    def get_base_n_intermediate_output(self, n, i):
        res = "" 

        for c in self.history[i]:
            res += c

        return np.base_repr(int(res, self.base), base=n)

    def get_population_size(self):
        return len(self.history[0])

    def get_rule(self):
        return self.rule

    def get_base(self):
        return self.base

    def produce_image(self, directory, n, legend=False, annot=False):
        res = list()

        for i in range(self.dimensions[0]):
            temp = list()

            for j in range(self.dimensions[1]):
                temp.append(int(self.history[n][(i * self.dimensions[1]) + j], base=self.base))

            res.append(temp)

        df_cm = pd.DataFrame(res)
        plt.figure(figsize = (self.dimensions[1], self.dimensions[0])) #(20,20)
        sn.heatmap(df_cm, annot=annot, cbar=legend, cmap=self.color_palette)  # sn.color_palette("viridis", self.base)

        if legend:
            plt.xlabel("Cell Number")
            plt.ylabel("Generation")
        
        plt.axis('off')

        plt.savefig(directory + str(n), bbox_inches='tight')
        plt.clf()
        plt.close('all')

        

    def generate_media(self, legend=False, annot=False, directory="./"):

        if len(self.dimensions) == 1:
            array = list()

            for gen in self.history:
                array.append(list([int(x, base=self.base) for x in gen]))

            df_cm = pd.DataFrame(array, index =list([x for x in range(len(self.history))]), columns =list([x for x in range(len(self.history[0]))]))
            plt.figure(figsize = (self.dimensions[0], len(self.history))) 
            sn.heatmap(df_cm, annot=annot, cbar=legend, cmap=self.color_palette)

            if legend:
                plt.xlabel("Cell Number")
                plt.ylabel("Generation")
            else:
                plt.axis('off')

            plt.savefig(directory + str(self.get_base())+ "-" + str(self.get_rule())+ "-" + str(self.get_population_size()), bbox_inches='tight')
        elif len(self.dimensions) == 2:
            image_folder = './temp_images/'
            os.mkdir(image_folder)

            ### Create all the images
            for i in range(len(self.history)):
                self.produce_image(image_folder, i, legend=legend, annot=annot)

            

            image_files = [os.path.join(image_folder,img) for img in os.listdir(image_folder) if img.endswith(".png")]
            clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=10)
            clip.write_videofile(directory + str(self.get_base())+ "-" + str(self.get_rule())[:10]+ "-" + str(self.get_population_size()) + '.mp4')

            for image in image_files:
                os.remove(image)

            os.rmdir(image_folder)
        else:
            print("Cannot generate graphics for data with the following dimensions", str(len(self.dimensions)) + "D", self.dimensions, "......yet")


    def __str__(self):
        first = ""  
        last = ""

        for c in self.history[0]:
            first += c

        for c in self.history[-1]:
            last += c

        first_10 = int(first, self.base)
        last_10 = int(last, self.base)

        return "CA Details:\n\n - Number Of Diimensions: " + str(len(self.dimensions)) + "\n - Rule: " + \
            str(self.rule) + "\n - Base: " + str(self.base) + \
            "\n - Neighborhood Size: " + str(self.neighborhood_size) + \
            "\n - Number of Iterations: " + str(len(self.history) - 1) + \
            "\n - Population Size: " + str(len(self.history[0])) + "\n\n" + \
            "Inputs:\n\n - Base_" + str(self.base) + ": " + first + "\n - Base_10: " + str(first_10) + \
            "\n\nOutputs:\n\n - Base_" + str(self.base) + ": " + last + "\n - Base_10: " + str(last_10) + \
            "\n\n------------DONE------------\n"
