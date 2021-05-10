#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Insert chain names in an output GROMACS file
"""
__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "PDB edit"

import sys
import os

def correct_pdb(input_file, input_chains, termination = "_fixed_chains.pdb"):

	"""
	Iterate over the pdb rows in order 
	"""
	possible_aa = ["ALA", "ARG", "ASN", "ASP", \
					"CYS", "ASX", "GLU", "GLN", \
					"GLX", "GLY", "HIS", "ILE", \
					"LEU", "LYS", "MET", "PHE", \
					"PRO", "SER", "THR", "TRP", \
					"TYR", "VAL", "HSE", "HSD", \
					"HSP"]
	opened_file = open(input_file, "r").readlines()
	output_name = input_file.split(".")[0] + termination
	started, chain_index = False, 0

	with open(output_name, "w") as output_file:
		for row in opened_file:
			row = row.replace("\n","")
			res_name = row[17:20]
			if row[0:4] == "ATOM" and res_name in possible_aa:
				res_number = int(row[22:26].replace(" ",""))
				chain_loc = row[21]
				new_row = list(row)
				if started == False:
					holder_res_number = res_number
					started = True
				if res_number > holder_res_number:
					holder_res_number = res_number
				if res_number < holder_res_number:
					chain_index += 1
					holder_res_number = res_number
				new_row[21] = input_chains[chain_index]
				new_row = "".join(new_row) + "\n"
				output_file.write(new_row)
				continue
			output_file.write(row + "\n")

"""
To call the script:
python fix_gromacs_chains.py [filename] [chain_1] [chain_2] [chain_3] [...]

Unlimited number of chains, make sure they are typed in the order they appear.
This will not work with unordred "pdb" files 
"""

pdb_file = sys.argv[1]
chains = sys.argv[2:]	

correct_pdb(pdb_file, chains)