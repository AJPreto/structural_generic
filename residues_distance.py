"""
Use the function process pdb on a pdb file, store as variable.
On this output, run the function return coords, also using two amino acid residues of choice, to measure
 (format resname_resnumber_chain)
Deploy euclidean distance on the output above.
Output:
Euclidean distance between alpha carbons
"""
import sys
import numpy as np

def process_pdb(input_file):

    opened_file = open(input_file, "r").readlines()
    for row in opened_file:
        if row[0:4] == "ATOM" and row[13:16].strip() == "CA":
            row = row.replace("\n","")
            yield row

def check_res(line,res):
    if line[17:20].strip() == res[0]:
        cond_1 = 1
    else:
        cond_1 = 0
    if line[22:26].strip() == res[1]:
        cond_2 = 1
    else:
        cond_2 = 0
    if line[21] == res[2]:
        cond_3 = 1
    else:
        cond_3 = 0
    cond = cond_1 * cond_2 * cond_3
    if cond == 1:
        return [line[30:38].strip(),line[38:46].strip(),line[46:54].strip()]

def euclidean_distance(input_coords_1, input_coords_2):

    base = 0
    for coord_1, coord_2 in zip(input_coords_1, input_coords_2):
        this_diff = float(coord_1) - float(coord_2)
        this_diff_squared = this_diff ** 2
        base += this_diff_squared
    root = base ** (1/2)
    return root

def return_coords(processed_pdb, test_res_1, test_res_2):

    test_res_1 = test_res_1.split('_')
    test_res_2 = test_res_2.split('_')
    holder_1 = None
    holder_2 = None
    for row in processed_pdb:
        hold_1 = check_res(row,test_res_1)
        hold_2 = check_res(row,test_res_2)
        if hold_1 != None:
            holder_1 = hold_1
        if hold_2 != None:
            holder_2 = hold_2
        if holder_1 != None and holder_2 != None:
            break
    return holder_1, holder_2

"""
Example of run
"""

processed_file = list(process_pdb("D1R_3sn6.pdb"))
res_1 = "ASN_168_A"
res_2 = "PHE_75_A"
coord_1, coord_2 = return_coords(processed_file, res_1, res_2)
print(euclidean_distance(coord_1, coord_2))
