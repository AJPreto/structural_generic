"""
Use the function process pdb on a pdb file, store as variable.
On this output, run the function execute on file to calculate the inter 
chain distance and yield a binary class
Output:
Binary interfacial class for dimer chain
"""
import sys
import numpy as np

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "CRADDLE"

def process_pdb(input_file):

    """
    Process the .pdb file making sure only the ATOM rows are considered 
    """
    opened_file = open(input_file, "r").readlines()
    for row in opened_file:
        if row[0:4] == "ATOM":
            row = row.replace("\n","")
            yield row

def euclidean_distance(input_coords_1, input_coords_2):

    """
    Measure the distance between two atom
    """
    base = 0
    for coord_1, coord_2 in zip(input_coords_1, input_coords_2):
        this_diff = float(coord_1) - float(coord_2)
        this_diff_squared = this_diff ** 2
        base += this_diff_squared
    root = base ** (1/2)
    return root


def execute_on_file(input_file):

    """
    Prepare a dictionary with the coordinates of all the atoms in the file
    """
    coordinates_dict = {}
    for row in input_file:
        if row[0:4] == "ATOM":
            row, chain_name = row.replace("\n",""), str(row[21]).replace(" ","")
            identifier = "_".join([str(row[17:20]), row[22:26].replace(" ",""), row[6:11].replace(" ","")])
            coordinates = [float(row[30:38]),float(row[38:46]),float(row[46:54])]
            if chain_name not in coordinates_dict.keys(): coordinates_dict[chain_name] = {}
            coordinates_dict[chain_name][identifier] = coordinates
    return coordinates_dict

def calculate_inter_chain(input_dictionary, threshold = 5):

    """
    Calculate inter-chain all atom contacts defined below a threshold
    """
    class_dictionary, current_amino_acid = {}, ""
    for atoms_A in input_dictionary["A"].keys():
        if current_amino_acid == "":
            amino_name = "_".join([atoms_A.split("_")[0], atoms_A.split("_")[1]])
            current_amino_acid = amino_name
        elif "_".join([atoms_A.split("_")[0], atoms_A.split("_")[1]]) != current_amino_acid:
            amino_name = "_".join([atoms_A.split("_")[0], atoms_A.split("_")[1]])
            if current_amino_acid not in class_dictionary.keys(): class_dictionary[current_amino_acid] = 0         
            current_amino_acid = amino_name
        for atoms_B in input_dictionary["B"].keys():
            distance = euclidean_distance(input_dictionary["A"][atoms_A], input_dictionary["B"][atoms_B])
            if distance < threshold:
                class_dictionary[current_amino_acid] = 1
    return class_dictionary

"""
Example of run
"""

processed_file = list(process_pdb("D1R-Gi1.pdb"))
all_coordinates = execute_on_file(processed_file)
usable_class = calculate_inter_chain(all_coordinates)
print(usable_class)