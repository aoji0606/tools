import os
import sys
import json
import random
from tqdm import tqdm
from pprint import pprint as pp

jsons = sys.argv[1:-1]
res = []
for file in jsons:
    data = json.load(open(file))
    res += data
    print(file, len(data))

print("res:", len(res))
# random.shuffle(res)
json.dump(res, open(sys.argv[-1], 'w'), indent=2, ensure_ascii=False)
print("save as:", sys.argv[-1])
