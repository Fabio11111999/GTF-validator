# @Author: Fabio Marchesi mtr 844841
# GTF-validator 
# GTF syntax: <seqname> <source> <feature> <start> <end> <score> <strand> <frame> [attributes] [comments]

import re, sys

# Validation part:
# Files and functions for the output of validation's results
validation = open("validation.txt", "w+")
successful_validation = True
def print_error(row, message):
	if row == 'x':
		return
	global successful_validation
	successful_validation = False
	validation.write('Validation failed.\n')
	if row != ' ':
		validation.write('Row ' + str(row) + ' : ' + message + '\n')
	else:
		validation.write(message + '\n')


# Function check_start_end(start, end, i)
# Boolean function that checks whether all these conditions are respected:
# start is an intger
# end is an integer
# end >= start
# start >= 1
def check_start_end(start, end, i):
	correct = True;
	try:
		int(start)
	except:
		print_error(i, 'Start value is not an integer')
		correct = False
	try:
		int(end)
	except:
		print_error(i, 'End value is not an integer')
		correct = False;
	if correct == True and int(end) < int(start):
		print_error(i, 'Start value is greater than end value')
		correct = False
	if correct == True and int(start) < 1:
		print_error(i, 'Start value is not greater than 0')
		correct = False
	return correct


# Function check_feature(feature, i)
# Boolean function that checks whether the feature's value is correct
# Feature must be equal to one of:
# ['CDS', 'start_codon', 'stop_codon', '5UTR', '3UTR', 'inter', 'inter_CNS', 'intron_CNS', 'exon']
def check_feature(feature, i):
	if feature not in ['CDS', 'start_codon', 'stop_codon', '5UTR', '3UTR', 'inter', 'inter_CNS', 'intron_CNS', 'exon']:
		print_error(i, 'Feature value is not valid, feature must be equal to: CDS or start_codon or stop_codon or 5UTR or 3UTR or inter or inter_CNS or intron_CNS or exon')
		return False
	return True


# Function check_strand(strand, i):
# Boolean function that checks whether the strand's value is correct on a single line
# Strand's value must be equal to '-' or '+'
def check_strand(strand, i):
	if strand not in ['-', '+']:
		print_error(i, 'Strand value must be "-" or "+"')
		return False
	return True


# Function check_score(score, i)
# Boolean function that checks wheter the score is a numeric value
def check_score(score, i):
	if score == '.':
		return True
	try:
		float(score)
	except:
		print_error(i, 'Score is not a numeric value')
		return False
	return True


# Function check_frame(feature, frame, i)
# Boolean function that checks whether the frame's value is correct
# If the feature is equal to one of: ['CDS', 'start_codon', 'stop_codon']
#	The frame must be equal to one of: ['0', '1', '2']
# Otherwise the frame must be equal to '.'
def check_frame(feature, frame, i):
	if feature in ['CDS', 'start_codon', 'stop_codon']:
		if frame not in ['0', '1', '2']:
			print_error(i, 'Frame value is not correct')
			return False
	else:
		if frame != ".":
			print_error(i, 'Frame value is not correct')
			return False
	return True
	

# Function list_attributes(s)
# Given a string return a list of pairs
# Every element is a pair(attribute, value)
def list_attributes(s):
	attributes = []
	while len(s) > 0:
		re_att = re.search('[^"]+', s) # Prefix before "
		if re_att == None:
			return []
		attribute = s[re_att.span()[0] : (re_att.span()[1] - 1)]
		s = s[len(attribute) + 2 : ] # Removing the space and "
		if len(s) > 0 and s[0] == '"': # Checking if value is empty
			s = s[1 : ]
			value = ""
		else:
			re_value = re.search('[^"]+', s) # Taking the value
			if re_value == None:
				return []
			value = s[ : re_value.span()[1]] 
			s = s[len(value) + 1 : ]
		attributes.append((attribute, value))
		if len(s) == 0 or s[0] != ';': # Wrong syntax
			return []
		if len(s) == 1:
			return attributes
		if s[1] != ' ' and s[1] != '\n':
			return []
		s = s[2 : ] # Remove '; '
	return attributes		


# Function check_attributes(feature, att, i)
# Boolean function that checks whether the attributes are correct
# gene_id and transcript_id must be present
# gene_id and transcript_id must be empty for gene = inter or gene = inter_CNS
def check_attributes(feature, att, i):
	elements = list_attributes(att)
	if elements == []:
		print_error('i', 'The list of attributes has the wrong syntax')
		return False
	if len(elements) < 2:
		print_error(i, 'Missing attributes, needded at least 2')
		return False	
	if elements[0][0] != 'gene_id':
		print_error(i, 'The first attribute (' + str(elements[0][0]) + ') must be "gene_id"')
		return False
	if elements[1][0] != 'transcript_id':
		print_error(i, 'The second attribute (' + str(elements[1][0]) + ') must be "Transcript_it"')
		return False
	if(feature in ['inter', 'inter_CNS'] and (elements[0][1] != '' or elements[1][1] != '')):
		print_error(i, 'gene_id and transcript_id must be equal to '' for features: inter and inter_CNS')
		return False
	return True


# Function check_row(row, i)
# Boolean function that checks whether the row is correct
# All the elements of a gtf's file row are checked 
def check_row(row, i):
	elements = row.split('\t')
	correct_row = True
	# Checking the number of values 
	correct_number_of_values = len(elements) >= 9
	if correct_number_of_values == False:
		print_error(i, "Not enough arguments")
		return False
	# Checking the feature
	correct_feature = check_feature(elements[2], i) 
	correct_row = correct_row and correct_feature
	# Checking start and end
	correct_start_end = check_start_end(elements[3], elements[4], i)
	correct_row = correct_row and correct_start_end
	# Checking the strand 
	correct_strand = check_strand(elements[6], i)
	correct_row = correct_row and correct_strand
	# Checking score
	correct_score = check_score(elements[5], i)
	correct_row = correct_row and correct_score
	# Checking the frame
	correct_frame = check_frame(elements[2], elements[7], i)
	correct_row = correct_row and correct_frame
	# Checking the attributes
	correct_attributes = check_attributes(elements[2], elements[8], i)
	correct_row = correct_row and correct_attributes
	return correct_row


# Function check_gene_strand(gtf_file_rows)
# Boolean function which checks if all the strands in the same gene are equal 
def check_gene_strand(gtf_file_rows):
	gene_dict = {}
	for i in range(len(gtf_file_rows)):
		row = gtf_file_rows[i]
		if check_row(gtf_file_rows[i], i) == True:
			elements = row.split('\t')
			current_strand = elements[6]
			current_attributes = list_attributes(elements[8])
			current_gene = current_attributes[0][1]
			if current_gene in gene_dict.keys():
				if(gene_dict[current_gene] != current_strand):
					print_error(i, 'Found a strand that does not match its gene strand')
					return False
			else:
				gene_dict[current_gene] = current_strand
	return True


# Function check_overlap(v)
# Boolean function that checks wheter or not a list of sorted intervals contains elements that overlap
def check_overlap(v): 
	if len(v) == 1:
		return True
	for i in range(len(v) - 1):
		if v[i][1] >= v[i + 1][0]:
			return False
	return True


# Function check_frame_gene(type, ranges, frames, transcript)
# Boolean function that checks if frames are good for start_codon/stop_codon/CDS
# type is the type of the sequence: start/stop/CDS
# ranges are the sorted intervals
# frames is a map that says for each interval its frame
def check_frame_gene(type, ranges, frames, transcript):
	length = 0
	for i in range(len(ranges)):
		start = ranges[i][0]
		end = ranges[i][1]
		frame = frames[(start, end)]
		try:
			int(start)
			int(end)
			int(frame)
		except:
			print_error(i, 'Start, End, Frame values must be integers')
			return False
		if(int(frame) != length):
			print_error(' ', 'Frame of interval [' + str(start) + ', ' + str(end) + '] of type ' + type + ' is not correct. Transcript = ' + transcript + ' Expected: ' + str(length) + " found: " + frame)
			return False
		length = (3 - (((end - start + 1) - length ) % 3)) % 3
	return True


# Function check_transcript(transcript)
# Boolean function that checks if a transcript is correct
# transcript is a sequence of row of the same transcript 
# for those row we have already checked that the strand is ok
def check_transcript(transcript):
	current_attributes = list_attributes(transcript[0].split('\t')[8])
	current_gene = current_attributes[0][1]
	current_transcript = current_attributes[1][1]
	strand = transcript[0].split('\t')[6]
	start_codons = []
	stop_codons = []
	ranges = []
	utr5 = []
	utr3 = []
	start_frame = {}
	stop_frame = {}
	CDS_frame = {}
	for row in transcript:
		elements = row.split('\t')
		feature = elements[2]
		start = elements[3]
		end = elements[4]
		frame = elements[7]
		if feature == 'start_codon':
			start_codons.append((int(start), int(end)))
			start_frame[(int(start), int(end))] = frame
		if feature == 'stop_codon':
			stop_codons.append((int(start), int(end)))
			stop_frame[(int(start), int(end))] = frame
		if feature == 'CDS':
			ranges.append((int(start), int(end)))
			CDS_frame[(int(start), int(end))] = frame
		if feature == '3UTR':
			utr3.append((int(start), int(end)))
		if feature == '5UTR':
			utr5.append((int(start), int(end)))

	# If there is not a CDS do not controll anything else
	if len(start_codons) + len(stop_codons) + len(ranges) == 0:
		return True
	# If there is a start_codon or stop_codon there must be a CDS and viceversa
	if len(start_codons) + len(stop_codons) + len(ranges) != 0 and len(start_codons) * len(stop_codons) * len(ranges) == 0:
		print_error(' ', 'If there is a start_codon or end_codon there must be a CDS and viceversa in transcript ' + current_transcript)
		return False
	# Checking if the lenght of start_codon is 3
	lenght_start_codon = 0
	for rangex in start_codons:
		lenght_start_codon = lenght_start_codon + rangex[1] - rangex[0] + 1
	if lenght_start_codon != 3:
		print_error(' ', 'Lenght of start_codon must be 3 in transcript ' + current_transcript)
		return False
	# Checking if the length of stop_codon is 3
	lenght_stop_codon = 0
	for rangex in stop_codons:
		lenght_stop_codon = lenght_stop_codon + rangex[1] - rangex[0] + 1
	if lenght_stop_codon != 3:
		print_error(' ', 'Lenght of stop_codon must be 3 in transcript ' + current_transcript)
		return False
	# Checking if the length of CDS is a multiple of 3
	lenght_CDS = 0
	for rangex in ranges:
		lenght_CDS = lenght_CDS + rangex[1] - rangex[0] + 1
	if lenght_CDS % 3 != 0:
		print_error(' ', 'Lenght of CDS must be a multiple of 3 in transcript ' + current_transcript)
		return False
	start_codons = sorted(start_codons)
	stop_codons = sorted(stop_codons)
	ranges = sorted(ranges)
	utr5 = sorted(utr5)
	utr3 = sorted(utr3)
	# Checking that ranges do not overlap for start_codons 
	if check_overlap(start_codons) == False:
		print_error(' ', 'Start_codons overlap in transcript ' + current_transcript)
		return False
	# Checking that ranges do not overlap for stop_codons 
	if check_overlap(stop_codons) == False:
		print_error(' ', 'Stop_codons overlap in transcript ' + current_transcript)
		return False
	# Checking that ranges do not overlap for CDS ranges 
	if check_overlap(ranges) == False:
		print_error(' ', 'CDS ranges overlap in transcript ' + current_transcript)
		return False
	# Checking that ranges of '5UTR' do not overlap
	if check_overlap(utr5) == False:
		print_error(' ', '5UTR ranges overlap in transcript ' + current_transcript)
		return False
	# Checking that ranges of '3UTR' do not overlap
	if check_overlap(utr3) == False:
		print_error(' ', '3UTR ranges overlap in transcript ' + current_transcript)
		return False
	if strand == '+':
		# Checking if start_codon is in a correct position 
		if len(start_codons) > 1:
			x = len(start_codons) - 1
			for i in range(x):
				if ranges[i] != start_codons[i]:
					print_error('', 'Start codons are not in the correct position in transcript ' + current_transcript)
					return False
		offset = len(start_codons) - 1
		if start_codons[offset][0] != ranges[offset][0]:
			print_error('', 'Start codons are not in the correct position in transcript ' + current_transcript)
			return False
		# Checking if stop_codon is in a correct position 
		if stop_codons[0][0] <= ranges[len(ranges) - 1][1]:
			print_error(' ', 'Stop_codons are not in the correct position in transcript ' + current_transcript)
			return False
		# Checking that 5UTR's segments come before the start codon
		if len(utr5) > 0 and start_codons[0][0] <= utr5[len(utr5) - 1][1]:
			print_error(' ', '5UTR segments are not before the start_codon in transcript ' + current_transcript)
			return False
		# Checking that 3UTR's segments go after the stop_codon 
		if len(utr3) > 0 and stop_codons[len(stop_codons) - 1][1] >= utr3[0][0]:
			print_error(' ', '3UTR segments are not after the stop_codon in transcript ' + current_transcript)
			return False
	else:
		# Checking if start_codon is in a correct position 
		if len(start_codons) > 1:
			x = len(start_codons) - 1
			for i in range(x):
				if ranges[len(ranges) - 1 - i] != start_codons[len(start_codons) - 1 - i]:
					print_error('', 'Start codons are not in the correct position in transcript ' + current_transcript)
					return False
		offset = len(start_codons) - 1
		if start_codons[0][1] != ranges[len(ranges) - 1 - offset][1]:
				print_error('', 'Start codons are not in the correct position in transcript ' + current_transcript)
				return False
		# Checking if stop_codon is in a correct position 
		if stop_codons[len(stop_codons) - 1][1] >= ranges[0][0]:
			print_error(' ', 'Stop_codons are not in the correct position in transcript ' + current_transcript)
			return False
		# Checking that 5UTR's segments come after the start codon (strand = '-')
		if len(utr5) > 0 and utr5[0][0] <= start_codons[len(start_codons) - 1][1]:
			print_error(' ', '5UTR segments are not after (strand = "-") the start_codon in transcript ' + current_transcript)
			return False	
		# Checking that 3UTR's segments go before the stop_codon (strand = '-')
		if len(utr3) > 0 and utr3[len(utr3) - 1][1] >= stop_codons[0][0]:
			print_error(' ', '3UTR segments are not before (strand = "-") the stop_codon in transcript ' + current_transcript)
			return False
	# Checking if the frames are correct
	if strand == '-':
		start_codons.reverse()
		stop_codons.reverse()
		ranges.reverse()
	if check_frame_gene('start_codon', start_codons, start_frame, current_transcript) == False:
		return False
	if check_frame_gene('stop_codon', stop_codons, stop_frame, current_transcript) == False:
		return False
	if check_frame_gene('CDS', ranges, CDS_frame, current_transcript) == False:
		return False



# Main Function: 
# Reading file's name and its lines
print('Starting GTF-validator')
print('Path to the file:')
gtf_file_name = input()
with open(gtf_file_name, 'r') as gtf_input_file:
	gtf_file_rows = gtf_input_file.readlines()
# Checking strands for the same gene
if check_gene_strand(gtf_file_rows) == False:
	print_error(' ', 'Impossibile to continue the validation bacause of this error')
	print('Validation Failed, open "Validation.txt" for more info')
	sys.exit(0)
# Group all the rows by gene and transcript
gene_transcript_dict = {}
different_transcripts = []
for i in range(len(gtf_file_rows)):
	row = gtf_file_rows[i]
	if check_row(row, 'x') == False:
		continue
	elements = row.split('\t')
	current_attributes = list_attributes(elements[8])
	current_gene = current_attributes[0][1]
	current_transcript = current_attributes[1][1]
	if (current_gene, current_transcript) in gene_transcript_dict.keys():
		current_index = gene_transcript_dict[(current_gene, current_transcript)]
		different_transcripts[current_index].append(row)
	else:
		gene_transcript_dict[(current_gene, current_transcript)] = len(different_transcripts)
		different_transcripts.append([row])

for transcript in different_transcripts:
	check_transcript(transcript)

if successful_validation == True:
	print('Correct Validation')
else:
	print('Validation Failed, open "Validation.txt" for more info')
