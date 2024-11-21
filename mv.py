import os
import sys
import random
from shutil import move
from tqdm import tqdm

src = sys.argv[1]
dst = sys.argv[2]
num = int(sys.argv[3])

files = os.listdir(src)
random.shuffle(files)
for file in tqdm(files[:num]):
    move(os.path.join(src, file), os.path.join(dst, file))
