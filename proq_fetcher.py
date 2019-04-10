#!/usr/bin/env python

"""
Access Proq with a pdb file to retrieve LGScore and MaxSub
Usage: python proq_fetcher.py [pdb_name] [secondary_structure]
If you do not wish to use secondary structure prediction,
 type None as the second argument
If you wish to use secondary structure prediction, 
the second argument is the string with the sequence prediction 
"""

import os
import requests
import sys

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "No specific project"

def interpret_output(input_response):
    
    """
    Filter out the LGScore and MaxSube values
    """
    response_by_row = input_response.split("BR")
    LGScore = response_by_row[2].split(":")[1][4:-5]
    MaxSub = response_by_row[3].split(":")[1][4:-5]
    print("LGSCore:",LGScore)
    print("MaxSub:",MaxSub)
    return LGScore, MaxSub

def proq_request(input_pdb, secondary_structure = None):

    """
    Use requests to retrieve the raw output
    """
    with requests.session() as current_sess:
        entry = current_sess.get(base_url)
        input_file = {'pdbfile':open(input_pdb, "rb")}
        if secondary_structure != None:
            input_data = {'ss': secondary_structure}
            response = current_sess.post(base_url, files=input_file, data = input_data)
        else:
            response = current_sess.post(base_url, files=input_file)
        raw_output = response.text
    return interpret_output(raw_output)

base_url = "https://proq.bioinfo.se/cgi-bin/ProQ/ProQ.cgi"
proq_request(sys.argv[1], sys.argv[2])
