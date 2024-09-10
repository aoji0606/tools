import json
import argparse
from tqdm import tqdm

argparse = argparse.ArgumentParser()
argparse.add_argument('path', type=str)
args = argparse.parse_args()
assert args.path.endswith('.jsonl')

lines = open(args.path).readlines()
res = []
for line in tqdm(lines):
    data = json.loads(line)
    res.append(data)
json.dump(res, open(args.path.replace(".jsonl", ".json"), 'w'), indent=2, ensure_ascii=False)

