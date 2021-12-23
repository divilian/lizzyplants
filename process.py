#!/usr/bin/env python

import sys

# Left to do:
# 1) Be smart about reading the letters of the various species directly from
# the file. (This will involve not merely using a single letter for the species
# name, since there will be duplicate "S"'s.)
# 2) Don't forget that we need to be smarter than just looking for "headers
# that start with a letter" since we have "CHROMNUM" and "POS" and "REF" in
# there.
# 3) Actually calculate the different Dxy's for the different pairs of species.
# (and figure out what to name them? They can't all literally be "Dxy".)
# 4) Move from CSV to tab-separated.

def build_row_dict(headings, values):
    ret_val = {}
    for i,h in enumerate(headings):
        ret_val[h] = values[i]
    return ret_val

def compute_Dxy(samples, species_letter1, species_letter2):
    species1 = [ v for k,v in samples.items() if k.startswith(species_letter1)
        and "." not in v ]
    species2 = [ v for k,v in samples.items() if k.startswith(species_letter2)
        and "." not in v ]

    num_comparisons = 0
    num_successes = 0

    for item1 in species1:
        for item2 in species2:
            num_comparisons += 1 
            if matches(item1, item2):
                num_successes += 1 
    if num_comparisons == 0:
        return 0.0
    return num_successes / num_comparisons
    
    
def compute_pi(samples):
    # Warning: pro-gamer move!
    nucleos = [ v for v in samples.values() if "." not in v ]

    num_comparisons = 0
    num_successes = 0
    for i in range(len(nucleos)):
        for j in range(i+1,len(nucleos)):
            if i != j:
                num_comparisons += 1
                if matches(nucleos[i], nucleos[j]):
                    num_successes +=1
    if num_comparisons == 0:
        return 0.0
    return num_successes / num_comparisons

def matches(n1, n2):
    if n1 == n2:
        return True
    if n1[2] == n2[0] and n1[0] == n2[2]:
        return True
    return False

def compute_pi_for_species(row_dict, species_letter):
    return str(compute_pi( { sample:row_dict[sample] for sample in row_dict if
        sample.startswith(species_letter) }))

def build_output_row(row_dict):
    output = row_dict['CHROMNUM'] + ","
    output += row_dict['POS'] + ","
    # TODO: figure out the letters yourself, big boy!
    output += ",".join([ compute_pi_for_species(row_dict,sl)
        for sl in ['S','E'] ]) + ","
    output += str(compute_Dxy(row_dict, "S", "E"))
    return output
    


if len(sys.argv) not in [2,3]:
    sys.exit("Usage: process.py inputFileName.txt [outputFileName.csv].")
elif len(sys.argv) == 2:
    input_filename = sys.argv[1]
    if not input_filename.endswith(".txt"):
        sys.exit("Input file must be in .txt format, and tab-separated.")
    output_filename = input_filename.replace(".txt", "_output.csv")
elif len(sys.argv) == 3:
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    

with open(input_filename,encoding="utf-8") as f:
    headings = f.readline().strip().split("\t")
    with open(output_filename, "w", encoding="utf-8") as of:
        print(headings[0] + "," + headings[1] + ",PI_E,PI_S,Dxy", file=of)
        lizzy = f.readline().strip().split("\t")
        while lizzy != ['']:
            row_dict = build_row_dict(headings, lizzy)
            output_row = build_output_row(row_dict)
            print(output_row, file=of)
            lizzy = f.readline().strip().split("\t")

print(f"Your output is now in {output_filename}.")
