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
