import sys
import json

name = sys.argv[1]
data = json.load(open(name))
print(len(data))
json.dump(data, open(name, 'w'), indent=2, ensure_ascii=False)
