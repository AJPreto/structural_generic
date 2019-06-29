#!/usr/bin/env python

"""
Center the coordinates of a .pdb file
"""

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"

def extract_coordinates(input_structure):

	"""
	Extract only the coordinates from the pdb file
	"""
	x_values, y_values, z_values = [], [], []
	for row in input_structure:
		row = row.replace("\n","")
		if row[0:4] == "ATOM":
			x_values.append(float(row[30:38]))
			y_values.append(float(row[38:46]))
			z_values.append(float(row[46:54]))
	return x_values, y_values, z_values

def calculate_average(input_coordinates):

	"""
	Calculate the coordinates' averages
	"""
	x_mean = sum(input_coordinates[0])/len(input_coordinates[0])
	y_mean = sum(input_coordinates[1])/len(input_coordinates[1])
	z_mean = sum(input_coordinates[2])/len(input_coordinates[2])
	return x_mean, y_mean, z_mean

def proper_length(input_value):

	"""
	Correct the coordinate fields to fit the standard pdb file format
	"""
	value = round(input_value,3)
	if len(str(value).split(".")[0]) == 1:
		value = "   " + str(value)
	elif len(str(value).split(".")[0]) == 2:
		value = "  " + str(value)
	elif len(str(value).split(".")[0]) == 3:
		value = " " + str(value)
	if len(str(value).split(".")[1]) == 0:
		value = value + "000"
	elif len(str(value).split(".")[1]) == 1:
		value = value + "00"
	elif len(str(value).split(".")[1]) == 2:
		value = value + "0"
	return str(value)

def replace_coordinates(input_structure, input_means, output_name = "test.pdb"):

	"""
	Write new pdb file with corrected coordinates
	"""
	with open(output_name, "w") as pdb_file:
		for row in input_structure:
			row = row.replace("\n","")
			if row[0:4] == "ATOM":
				x_val = float(row[30:38]) - input_means[0]
				y_val = float(row[38:46]) - input_means[1]
				z_val = float(row[46:54]) - input_means[2]
				new_row = row[0:30] + proper_length(x_val) + proper_length(y_val) + proper_length(z_val) + row[54:] + "\n"
			else:
				new_row = row + "\n"
			pdb_file.write(new_row)

def center_object(input_pdb, output_name):

	"""
	Deploy the pipeline
	"""
	opened_file = open(input_pdb, "r").readlines()
	coordinates = extract_coordinates(opened_file)
	coordinates_averages = calculate_average(coordinates)
	replace_coordinates(opened_file, coordinates_averages, output_name)
