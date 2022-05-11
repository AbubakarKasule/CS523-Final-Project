<<<<<<< HEAD
# import os
# import moviepy.video.io.ImageSequenceClip
# import PIL.Image
# from moviepy.editor import *



# PIL.Image.MAX_IMAGE_PIXELS = 933120000

# image_folder='./temp_images/'
# fps=24

# image_files = [os.path.join(image_folder,img)
#                for img in os.listdir(image_folder)
#                if img.endswith(".png")]
# print("Files loaded")

# clips = [ImageClip(m).set_duration(1) for m in image_files]
# print("INT")
# concat_clip = concatenate_videoclips(clips, method="compose")
# print("Movie Compiled")
# concat_clip.write_videofile("beeeg_video.mp4", fps=24) 



# clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
# print("Movie Compiled")
# clip.write_gif('beeeg_video.gif')
#import Utils
#print(len(Utils.PALETTES))  #170
import multiprocessing as mp
from multiprocessing import Pool
import time
def f(x):
    if x == 6:
        return 88
    return x


with Pool(20) as p:
    x = p.map(f, list(range(10)))

print(x)
=======
import sys
import numpy as np
import Utils
import os
import moviepy.video.io.ImageSequenceClip
#print(int(np.base_repr(sys.maxsize, base=16) * 2, 16))


#print(int("F"*99999, base=16))

# print(Utils.get_num_of_rules(5, 5))

image_folder = './temp_images/'

image_files = [os.path.join(image_folder,img) for img in os.listdir(image_folder) if img.endswith(".png")]
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=1)
clip.write_videofile('video.mp4')
>>>>>>> 8ec9b488608a431959362cd22e70126ef0eaa650
