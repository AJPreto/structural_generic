#!/usr/bin/env python

"""
This script will open a pdb and replace the b factor with conservation values.
These values come from a consurf run. Finally, a pdb output is written
"""

import csv
import os

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "No specific project"


def open_consurf(input_consurf_file):

    """
    Open and retrieve the consurf file. Note that the only
    rows starting with numbers are of interest.
    """
    opened_file = open(input_consurf_file, "r").readlines()
    for row in opened_file:
        row = row.replace("\n","")
        new_row = row.split()
        try:
            if type(int(new_row[0])) == int:
                yield (new_row[0], new_row[4].replace("*",""))
        except:
            continue


def open_pdb(input_pdb, input_single_chain, consurf_output, consurf_prefix = "consurf_corrected_"):


    """
    Read the pdb, open consurf, fetch corresponding value, and write new pdb.
    """
    pdb_location = home + "/" + input_pdb
    output_name = home + "/" + consurf_prefix + input_pdb
    opened_pdb = open(pdb_location,"r").readlines()
    chain_holder = {}
    number_holder = 0
    positive_corrector = 0
    correction_made = False
    output_file = open(output_name, "w")
    for row in opened_pdb:
        original_row = row
        row = row.replace("\n","")
        identifier = row[0:4]
        if identifier == "ATOM":
            res_number = row[22:26].replace(" ","")
            chain = row[21].replace(" ","")           
            occupancy = float(row[54:60].replace(" ",""))
            temp = float(row[60:66].replace(" ",""))
            if chain == input_single_chain:
                to_write_row = original_row[0:54] + "    " + str(consurf_output[int(res_number) - 1][1]) + "    " + str(consurf_output[int(res_number) - 1][1]) + "\n"
                output_file.write(to_write_row)


"""
Global variables, change depending on your data
"""
home = "C:/Users/marti/OneDrive/Desktop"
input_pdb = "stargazin_pdb_With_Conservation_Scores.pdb"
consurf_file = "consurf.txt"


"""
First run open_consurf inside a list (otherwise it is just a generator)
Then call open pdb with you protein, the chain and the corresponding consurf processed file
"""
processed_consurf = list(open_consurf(consurf_file))
print(open_pdb(input_pdb, "A", processed_consurf))