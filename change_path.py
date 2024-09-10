import os
import sys
import json
import random
from tqdm import tqdm
from pprint import pprint as pp


data = json.load(open(sys.argv[1]))
res = []
for i in tqdm(data):
    if "image" not in i:
        res.append(i)
        continue

    i["image"] = "Eagle-1.8M/" + i["image"]
    res.append(i)
    
json.dump(res, open("res.json", 'w'), indent=2, ensure_ascii=False)

