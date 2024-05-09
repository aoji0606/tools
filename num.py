import os
import sys

num = 0
for root, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        num += 1
print(num)
