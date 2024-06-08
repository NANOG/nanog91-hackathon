#!/usr/bin/env python3
import sys
import pdb
import hashlib

chars_to_strip = [" ", "\n", "\r", "\t"]
filename = sys.argv[1]

with open (filename, "r") as f:
    try:
        solution_text = f.read()
    except IOError as e:
        sys.exit("Error reading file f: {e}")
    
#pdb.set_trace()    
for char in chars_to_strip:
    new_solution_text = solution_text.replace(char, "")
    solution_text = new_solution_text
    
print(hashlib.md5(solution_text.encode('utf-8')).hexdigest())