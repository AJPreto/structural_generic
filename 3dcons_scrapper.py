#!/usr/bin/env python
"""
From a pdb id list fetch the PSSM profiles from 3dcons
"""

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "Protein-Ligand"

DCONS_URL = "http://3dcons.cnb.csic.es/pssm_json"
INTERMEDIATE_SEP = "_"
SYSTEM_SEP = "/"
AMINO_ACIDS_CONVERTER = {"A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", \
                                        "C": "CYS", "B": "ASX", "E": "GLU", "Q": "GLN", \
                                        "Z": "GLX", "G": "GLY", "H": "HIS", "I": "ILE", \
                                        "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", \
                                        "P": "PRO", "S": "SER", "T": "THR", "W": "TRP", \
                                        "Y": "TYR", "V": "VAL"}

def save_json(input_response, entry_name, \
                download_loc = ""):

    """
    Write the json response onto an output_file
    """
    if download_loc != "":
        output_name = download_loc + SYSTEM_SEP + entry_name + ".json"
    elif download_loc == "":
        output_name = entry_name + ".json"
    with open(output_name, "w") as json_output:
        json_output.write(input_response.text)

def process_json(input_response, multiple_chains = False, iter_num = 3):

    """
    Process the json response
    If the input is a single chain, the output is a pandas dataframe with the PSSM results, 
    otherwise, it is a dictionary in which the keys are the chain names and the values the respective PSSM results 
    """
    def process_single_chain(input_object, iter_num = 3):

        """
        Process the chain to yield a pandas dataframe
        """
        import pandas as pd
        output_table = []
        for index, row in enumerate(input_object):
            current_res_number, current_res_name = row["res_id"], AMINO_ACIDS_CONVERTER[row["aa"]]
            current_row = row["iter"][str(iter_num)]
            row_pssm = current_row["pssm"]
            row_psfm = current_row["psfm"]
            row_a, row_b = current_row["a"], current_row["b"]
            full_row = [index, current_res_number, current_res_name] + row_pssm + row_psfm + [row_a, row_b]
            output_table.append(full_row)
        header = ["indexed_number","original_residue_number","residue_name"] + \
                    ["pssm_" + str(x) for x in range(1,21)] + \
                    ["psfm_" + str(x) for x in range(1,21)] + \
                    ["a", "b"]
        return pd.DataFrame(output_table, columns = header)

    if multiple_chains == True:
        chains_dictionary = {}
        chains_list = list(input_response)
        for entry in chains_list:
            chains_dictionary[entry] = input_response[entry]
        output_dictionary = {}
        for current_chain in chains_list:
            output_dictionary[current_chain] = process_single_chain(chains_dictionary[current_chain])
        return output_dictionary

    elif multiple_chains == False:
        current_table = process_single_chain(input_response)
        return current_table

def scrape_3dcons(input_entry, single_chain_mode = False,
                    download_loc = "", \
                    current_url = DCONS_URL, \
                    save_mode = False, \
                    iter_num = 3):

    """
    Access 3dcons to retrieve the pssm format
    """
    import requests
    if single_chain_mode == False:
        query_url = DCONS_URL + SYSTEM_SEP + input_entry
    elif single_chain_mode == True:
        query_url = DCONS_URL + SYSTEM_SEP + input_entry.split(INTERMEDIATE_SEP)[0] + \
                        SYSTEM_SEP + input_entry.split(INTERMEDIATE_SEP)[1]
    current_response = requests.get(query_url)

    if save_mode == True:
        save_json(current_response, input_entry, \
                    download_loc = download_loc)
    if single_chain_mode == True:
        results = process_json(current_response.json(), multiple_chains = False, \
                        iter_num = iter_num)
    elif single_chain_mode == False:
        results = process_json(current_response.json(), multiple_chains = True, \
                        iter_num = iter_num)
    return results
        
"""

#Example 1 - Retrieve the PSSM results for a specific PDB code
##Output a dictionary with the chains as keys and the pandas dataframes as values
current_pdb = "3sn6"
current_table = scrape_3dcons(current_pdb, \
                single_chain_mode = False)

#Example 2 - Retrieve the PSSM results for a specific PDB chain
##Outputs a single pandas dataframe
current_pdb_chain = "3sn6_A"
current_table = scrape_3dcons(current_pdb_chain, \
                single_chain_mode = True)
"""

