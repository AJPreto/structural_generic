#!/usr/bin/env python

"""
Calculate RMSD between a reference pdb and all the remaining pdbs in the folder.
Steps:
1 - change the reference_name to your template pdb
2 - open pymol
3 - in pymol, if you are not in the folder of this script, go to folder (using bash commands)
4 - in pymol shell type "run calculate_rmsd.py"
5 - check the output file ("default: output_rmsd.csv")

WARNING: output file is overwriting, you will need to erase it between runs or, if you want to try different templates,
copy it elsewhere and then erase it
"""

from pymol import cmd
from glob import glob

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"

def perform_alignment(template, test_pdb, output_file = "output_rmsd.csv"):

    """
    Perform and alignment using PyMOL's python API
    """
    opened_file = open(output_file,"a")
    cmd.load(template,"template")
    cmd.load(test_pdb,"other")
    rms = cmd.align("template","other")[0]
    to_write_row = template[0:-4] + "," + test_pdb[0:-4] + "," + str(rms) + "\n"
    opened_file.write(to_write_row)
    cmd.delete("other")

def perform_multiple_alignments(avoid):

    """
    Deploy the alignment on all the .pdb files in the folder
    """
    for files in os.listdir(os.getcwd()):
        if files.endswith(".pdb") and (files != avoid):
            perform_alignment(avoid, files) 

#reference_name = "2rhk_A.pdb"
#perform_multiple_alignments(reference_name)