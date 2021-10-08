#!/usr/bin/env python 
## script written by D. Schmidt (danielle.schmidt@ubc.ca)
## Purpose: Convert GT-seq compiled output (.csv) and converts to .ped file (no map file though). Includes hashed out block of code for including a header line for the resulting .ped file in case of troubleshooting.
## Takes input of gtseq output in .csv format and a sample info .txt file (no header) that includes fam_id\t sample name\t sample barcode, as well as the list of loci included in your data (should match the IDs in the GT-seq output).

import re
import sys

input('\n'+"Get pysched to convert your genotypic data to anaylze it!")
Gtseq=input('\n'+"What's the name of your GTseq output file (including file extension?)"' ')
input('\n'+ "Thanks, yo!")
Samp_info=input('\n'+"What's the name of your sample information file (including extension?)"' ')
order_input= input('\n'+"Add list to specify locus order in .ped file output"' ')
outfile= input('\n'+"What do you want your output .ped file to be called (including .ped extension)?!"' ')

GTseq_out= open(Gtseq,'r').readlines() # GT-seq .csv output from pipeline
ID_info=open(Samp_info,'r').readlines() # Text file containing location, sample ID, and associated barcode for sample
PED= open(outfile, 'w')# Turning it all into a .ped file eventually
order= open(order_input,'r').readlines()

#create dictionaries to match up the family ID (i.e. location) of each sample to the sample name and associated barcode
ID_match= {}
samp_IDs={}
for line in ID_info:
	# I split these statements so that the line endings would come off and the dictionary wouldn't mess up
	line=line.replace('\n','')
	line=line.replace('\r','')
	IDs=line.split('\t')
	ID_match[IDs[2]]=IDs[0]
	samp_IDs[IDs[2]]=IDs[1]

#make locus order_list
order_list=[]
for locus in order:
	locus=locus.replace('\r', '')
	locus=locus.replace('\n','')
	order_list.append(locus)

#start with the header line to help count the number of SNP loci in the file
firstLine = GTseq_out.pop(0)# look at only the header
firstLine=firstLine.strip('\n')
firstLine=firstLine.strip('\r')# \r\n line endings removed. 
cols=firstLine.split(',')
#print (cols) #print list of loci in the GT-seq compiled output
for x in range(6):
    cols.pop(0) 

header_dict={}
num=6 
for locus in cols:
	header_dict[locus]=num
	num+=1
    
num_loci= len(header_dict)# total number of loci present in data [to help validate while file types are translating]
print ('\n'+"No. loci in file equal to "+ str(num_loci)) #lets you know the number of loci in your input file

#set header values
#famID= "famID"
#sampID= "Sample ID"
#M= "M"
#F= "F"
#Sex= "sex"
#Phenotype= "phenotype" 
#info= famID+'\t' +sampID+'\t' +M+'\t'+F+'\t' +Sex+'\t'+Phenotype+'\t'

# print header values to .ped file
#PED.write(info)

#duplicate locus headers (to make one column per allele)
locus_no=1
for locus in order_list: 
	print('\n'+"Working on locus "+str(locus_no)+": "+locus)
	#PED.write(locus+'\t'+locus+'\t') # duplicate locus ID
	locus_no+=1
#PED.write('\n') #start a new line for actually filling in the columns with genotypes	

#back to the rest of the GTseq file....
for line in GTseq_out:	
	line= line.replace('\r\n','')
	cols_2=line.split(",") #split each line into components of each column
	famID_2= ID_match[cols_2[0]] #grab associated location depending on barcode ID (which is the first column in the GTseq output file)
	sampId_2= samp_IDs[cols_2[0]] #grab sample name from associated barcode (also going off of the value in the first column of the GTseq output file)
	
# define the other placeholder values...
	M_2="0"
	F_2="0"
	Sex_2="0"
	Phenotype_2= "-9"
	info_2= famID_2+'\t'+sampId_2+'\t'+M_2+'\t'+F_2+'\t'+Sex_2+'\t'+Phenotype_2+'\t'
	PED.write(info_2) # fill in first 6 columns 

#start filling in genotypes
	for locus in order_list: #same as above
		nom=header_dict[locus]	
		gt= list(cols_2[nom]) #take each genotype and make it a list so it can be parsed apart to fill columns. Note: missing genotypes only have one 0 total in the input, not one 0 for each missing allele
		if len(gt)==1: #i.e. if data is missing and there are only 0s:
			PED.write(gt[0]+'\t'+gt[0]+'\t') #write each 0 in a separate column, one right after the other
		else: #everything else that doesn't have missing data will have 2 alleles, so then these get printed (i.e. GG becomes G \t G)
			PED.write(gt[0]+'\t'+gt[1]+'\t')
	PED.write('\n') # end the line and move onto the next	
print ('\n'+"All done!")
PED.close()
#DONE!
