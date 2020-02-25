#!/usr/bin/env python

"""
Query table from uniprot ID
"""

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = ""

import os
import pandas as pd
import sys
from variables_scrape_uniprot_pdb import SYSTEM_SEP, SEP, HOME, INPUT_FILE, \
						RAW_SEP, UNIPROTID_COLUMN, UNIPROTID_QUERY_START, \
						UNIPROT_WEBLINK, FASTA_TERMINATION, UNIPROT_SEP, \
						PBD_DOWNLOAD_URL, UTF_ENCODING, SEQUENCE_COLUMN, \
						OUTPUT_NAME, PDBS_COLUMN, PDB_FORMAT
from Bio.PDB import *

def opened_file(input_csv):
	"""
	Process_
	"""
	return pd.read_csv(input_csv, sep = RAW_SEP, header = 0)

def extract_sequence(input_query):

	"""
	Download Uniprot sequence and ID
	"""
	import requests as r
	from Bio import SeqIO
	from io import StringIO

	query_url = UNIPROT_WEBLINK + input_query + FASTA_TERMINATION
	response = r.post(query_url)
	server_data = ''.join(response.text)
	sequence = StringIO(server_data)
	sequence_object = list(SeqIO.parse(sequence,FASTA_TERMINATION[1:]))
	return sequence_object[0].seq, sequence_object[0].id.split(UNIPROT_SEP)[1]

def query_pdb(input_id):

	"""
	Query PDB to check if it has a match on a Uniprot ID and, if so, to download the structure
	"""
	import urllib.parse
	import urllib.request
	
	params = {
	"from": "ACC+ID",
	"to": "PDB_ID",
	"format": "tab",
	"query": input_id
	}

	data = urllib.parse.urlencode(params)
	data = data.encode(UTF_ENCODING)
	req = urllib.request.Request(PBD_DOWNLOAD_URL, data)
	with urllib.request.urlopen(req) as f:
	   response = f.readlines()
	pdbs_list =[]
	for row in response:
		single_pdb = row.decode(UTF_ENCODING).replace("\n","").split("\t")[1]
		pdbs_list.append(single_pdb)
	pdbl = PDBList()
	os.mkdir(input_id)
	for entry in pdbs_list[1:]:
		pdbl.retrieve_pdb_file(entry, pdir = input_id, file_format = PDB_FORMAT)
	return pdbs_list[1:]

def generate_output_table(input_table, output_name = OUTPUT_NAME):

	"""
	Iterating over input_table, generate output table with query from Uniprot and PDBids
	"""
	pdb_ids_column, sequences_column = [], []
	count = 0
	for index, row in input_table.iterrows():
		count += 1
		print("Current row", count, "/", input_table.shape[0])
		proper_query = row[UNIPROTID_COLUMN] + UNIPROTID_QUERY_START
		sequence, uniprot_id = extract_sequence(proper_query)
		sequences_column.append(str(sequence))
		output_pdbs = query_pdb(uniprot_id)
		pdb_ids_column.append(output_pdbs)
	input_table[SEQUENCE_COLUMN] = sequences_column
	input_table[PDBS_COLUMN] = pdb_ids_column
	input_table.to_csv(output_name, index = False, sep = SEP)


opened_dataframe = opened_file(INPUT_FILE)
generate_output_table(opened_dataframe)