from imagededup.methods import PHash, AHash, WHash, DHash, CNN
from imagededup.utils import plot_duplicates
import os
import json
import numpy as np
from PIL import Image

pHasher = PHash()
#aHasher = AHash()


#########find duplicate for each image###########

# duplicates = pHasher.find_duplicates(image_dir='/mnt/c/Users/galil/test', 
#                                                max_distance_threshold=12,
#                                                recursive=True,
#                                                scores=True,
#                                                outfile='my_duplicates.json')

##########find only duplicate photos############