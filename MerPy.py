import glob
import mer_class as mer

import pandas as pd
file_path = '/home/umar/python programming files/enrichment_analysis_paper/clustering_result_files/cluster0rel_max.csv'
#gene_file.head(5)
gene_file = pd.read_csv(file_path)
gene_symbols_list = list(gene_file['ALIAS'])
gene_symbols_list
len(gene_symbols_list)
#function calling
mer.get_medline_abstracts_ncbi(gene_symbols_list)

'''
# read the input gene file
with open("input_terms.txt", "r") as input_handle:
	terms_list = input_handle.readlines()
#create files of title and abstarct for given genes
if mer.get_medline_abstracts_ncbi(terms_list):
	print("data downloaded")
	# Store the name of all files in a list
else:
	print("Error in download")
'''


#output file name
result_file_name = '/home/umar/python programming files/enrichment_analysis_paper/mer_result/mer_cluster0_result.txt'

gene_file_list = []
for i in gene_symbols_list:
	#print(i +'.txt')
	gene_file_list.append(i+'.txt')
gene_file_list
len(gene_file_list)

#read the created files
#gene_file_list = [f for f in glob.glob("*.txt")]
#print('Files found in folder: ', gene_file_list)
import multiprocessing as mp
import time
start_time = time.time()

#pool = mp.Pool(processes=4)
#results = [pool.apply_async(mer.perom_mer_mp, args=(countt, f, result_file_name)) for countt, f in enumerate(gene_file_list, 1)]
#output = [p.get() for p in results]
#print(output)


for countt, f in enumerate(gene_file_list, 1):
	out_mer = mer.perom_mer_mp(countt, f, result_file_name)
	print(out_mer, "file written")

print("--- %s seconds ---" % (time.time() - start_time))


# to remove duplicated line sin the file
# need to be checked
#file_uniqlines = set(open('out_mer').readlines())
#final_out_file = open('Final_output.txt', 'w').writelines(set(file_uniqlines))
#final_out_file.close()


''' Wokring merpy
import merpy
merpy.generate_lexicon("hp")

def merpy_function(article_abstract):
	document = article_abstract
	entities = merpy.get_entities(document, "hp")
	return entities


def output_file_function(article_title, gene_term, merpy_res_nested_list):
	with open("results_merpy.txt", "a") as res_file:
		for g in merpy_res_nested_list:
			res_file.write(article_title + "," + gene_term + "," + g[2] + "," + g[3] + "\n")

    #return True check this why its not wroking


with open(gene_term + ".txt", "r") as in_file:
    lines = in_file.readlines()

for k in lines:
    line = k.split("___")
    article_title = line[0]
    article_abstract = line[1]
    merpy_res_nested_list = merpy_function(article_abstract)
    output_file_function(article_title, gene_term, merpy_res_nested_list)

    print(merpy_res_nested_list, "printing merpy arrays")


'''


import numpy as np
print(3)
