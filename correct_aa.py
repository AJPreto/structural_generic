#!/usr/bin/env python

"""
Change a ".pdb" file amino acid name
"""

import os

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "No specific project"

def open_pdb(input_pdb_file):

    """
    Generator yielding a simple processed pdb file
    """
    opened_pdb = open(input_pdb_file, "r").readlines()
    for row in opened_pdb:
        row = row.replace("\n","")
        yield row

def correct_pdb(input_pdb_file, erase_original = False, target_aa = "HSD", correct_aa = "HIS"):

    """
    Iterate over a pdb file and replace the "target_aa" with "correct_aa".
    If you want to erase the original, call "erase_original" as True.
    """
    output_pdb_file = "corrected_" + input_pdb_file
    with open(output_pdb_file, "w") as corrected_file:
        for row in open_pdb(input_pdb_file):
            if row[0:4] == "ATOM":
                amino_acid = row[17:20]
                if amino_acid == target_aa:
                    corrected_AA = correct_aa
                    corrected_row = row[0:17] + correct_aa + row[20:] + "\n"
                else:
                    corrected_row = row + "\n"
                corrected_file.write(corrected_row)
            else:
                raw_row = row + "\n"
                corrected_file.write(raw_row)
    if erase_original == True:
        os.remove(input_pdb_file)
        os.rename(output_pdb_file, input_pdb_file)

def apply_on_folder(target_folder = os.getcwd()):

    """
    Correct all the files in a "target_folder".
    The target_folder can be changed upon calling the function.
    The originals wiil be erased and the "HSD" amino acids will be changed
    to "HIS" by default
    """

    for files in os.listdir(target_folder):
        if files.endswith(".pdb"):
            correct_pdb(files, erase_original = True)

"""
Use:

apply_on_folder()

to change all the files in the folder

Use:

correct_pdb("example.pdb", erase_original = False, target_aa = "HSD", correct_aa = "HIS")

to change a single ".pdb" file

"""