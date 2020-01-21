#!/usr/bin/env python

"""
Renumber a pdb file to start from 1
"""

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"

def renumber_pdb(input_path, replace_file = False, termination = ".pdb"):

	"""
	The activation of the argument replace_file to True
	completely erases the original file, be careful when using
	"""
	opened_pdb = open(input_path, "r").readlines()
	output_name = input_path.split(".")[0] + "_temp" + termination
	started = False
	with open(output_name, "w") as write_file:
		for row in opened_pdb:
			row = row.replace("\n","")
			if row[0:4] == "ATOM":
				if started == False:
					count = 1
					holder_res = int(row[22:26])
					current_res = count
					started = True
				if int(row[22:26]) != holder_res:
					holder_res = int(row[22:26])
					count += 1
					current_res = count
				proper_row = row[0:22] + str(current_res).rjust(4) + row[26:] + "\n"
			else:
				proper_row = row + "\n"
			write_file.write(proper_row)
	if replace_file == True:
		import os
		os.remove(input_path)
		os.rename(output_name, input_path)

"""
Example of how to use below
"""
#renumber_pdb("pdb1eaw.ent", termination = ".ent", replace_file = True)