#!/usr/bin/env python

"""
This script transforms a clustal omega alignment output to a
 modeller .ali output. Usable for only two aligned sequences
"""
import textwrap
import csv
import os

__author__ = "A.J. Preto"
__email__ = "martinsgomes.jose@gmail.com"
__group__ = "Data-Driven Molecular Design"
__group_leader__ = "Irina S. Moreira"
__project__ = "No specific project"

def generate_seq(input_alignments, input_start):

	"""
	Extract a sequence from the alignment, warning,
	only works with two sequences, otherwise the 
	skip step of range must be changed
	"""
	sequence = ""
	for row in range(input_start,len(input_alignments),4):
		new_row = input_alignments[row].replace("\n","") 
		sequence += new_row.split()[1]
	return new_row.split()[0], sequence

def generate_seq_block(input_sequence):

	"""
	Prepare each block to be written.
	Warning: you may want to manually change the sequence headers
	"""
	header = "\n>P1;" + input_sequence[0] + "\n"
	sequence_name = "sequence:" + input_sequence[0] + ":1    : :0 : ::: 0.00: 0.00" + "\n"
	target_sequence = input_sequence[1] + "*"
	sequence = [target_sequence[i:i+75] for i in range(0, len(target_sequence), 75)]
	final_string = header + sequence_name
	for row in sequence:
		final_string += row + "\n"
	return final_string


def write_ali(input_seq_A, input_seq_B):

	"""
	Write the .ali file
	"""
	output_name = input_seq_A[0] + "_" + input_seq_B[0] + ".ali"
	opened_output = open(output_name,"w")
	opened_output.write(generate_seq_block(input_seq_A))
	opened_output.write(generate_seq_block(input_seq_B))


def open_file(input_file):

	"""
	Open the input Clustal file and write the output
	"""
	opened_file = open(input_file, "r").readlines()[3:]
	seq_A = generate_seq(opened_file, 0)
	seq_B = generate_seq(opened_file, 1)
	write_ali(seq_A, seq_B)



input_file = "alignment_example.clustal_num"
open_file(input_file)