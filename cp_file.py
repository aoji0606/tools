import os
import sys
import random
from shutil import copy
from tqdm import tqdm

src = sys.argv[1]
dst = sys.argv[2]
num = int(sys.argv[3])

files = os.listdir(src)
random.shuffle(files)
for file in tqdm(files[:num]):
    copy(os.path.join(src, file), os.path.join(dst, file))
