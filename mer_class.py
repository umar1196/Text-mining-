from Bio import Entrez
from Bio import Medline
# to pick names of files in directory
import glob
import merpy

merpy.generate_lexicon("hp")


def get_medline_abstracts_ncbi(terms_list):
    '''
    given a genes list downloads the abstracts from medline pubmed. fetches maximum number of abstracts for given gene and
    store it in .txt file with name of input gene. To make one line combines each abstract with title  by "___".
    :param terms_list: lis of genes
    :return: True if all files are created
    '''
    cc = 1  # increment to tell how many genes left
    #out_dir = "C:/Users/muh_asif/PycharmProjects/parellel/Clustering_genes/Results/Rel_max_2019-05-16_.txt__data_frame_with_NA_gene_symbol_backup/pap/"

    try:
        for term in terms_list:
            gene_term = term.strip()
            print("processing", gene_term)

            handle = Entrez.esearch(db="pubmed", term=gene_term, retmax=10000)
            record = Entrez.read(handle)
            handle.close()

            idlist = record["IdList"]

            print(len(idlist), "articles found for", gene_term, " and will be downloaded")

            handle = Entrez.efetch(db='pubmed', id=idlist[:10], retmode='text', rettype='medline')
            records = Medline.parse(handle)
            records = list(records)
            # gene output file
            #out_gene_file = out_dir + gene_term + ".txt"
            out_gene_file =  gene_term + ".txt"

            with open(out_gene_file, "w") as file:

                for record in records:
                    file.write(str(record.get("TI")) + "___" + str(record.get("AB")) + "\n")
            file.close()

            print(out_gene_file, "file is written with total abstarcts: ", len(idlist))
            print("remaining input genes: ", len(terms_list) - cc, "\n")
            cc = cc + 1
        return True

    except Exception as e:
        print(e.message, e.args)



def merpy_function(article_abstract):
    '''
    Run MER. terms are inialized in the beginning of script with line: merpy.generate_lexicon("hp")
    :param article_abstract:  variable containing the abstract text
    :return: a nested list with identified term, its position and url of term
    '''
    document = article_abstract
    entities = merpy.get_entities(document, "hp")

    return entities


def output_file_function(article_title, gene_term, merpy_res_nested_list):
    '''
    writes resulatnt file
    :param article_title: title of article
    :param gene_term: gene name
    :param merpy_res_nested_list: output from MER
    :return:
    '''
    with open("results_merpy.txt", "a") as res_file:
        for g in merpy_res_nested_list:
            res_file.write(article_title + "," + gene_term + "," + g[2] + "," + g[3] + "\n")


# return True check this why its not wroking

def perom_mer(gene_file_list, result_file_name):
    '''
    Given a list of file names (containing title and abstracts for gene) performs MER analysis and write results into output file
    :param gene_file_list: names of gene files containing title and abstracts for gene. each line of file is title___absract
    :param result_file_name:
    :return: name of resulatnt file that is written
    '''

    result_file = result_file_name

    for countt, f in enumerate(gene_file_list, 1):

        f_gene = str(f.split(".")[0])  # pick the gene name
        f_gene = f_gene.strip(' ')
        print(f, "file name")
        print(f_gene, "gene name")
        with open(f, "r") as in_file:
            lines = in_file.readlines()  # .replace('\n', '')
            # print(lines)
            for l in lines:
                line = l.split("___")
                # article_abstract = line[1].strip(' ')
                article_abstract = line[1].strip(' ')

                merpy_res_nested_list = merpy_function(article_abstract)
                # print(merpy_res_nested_list)
                article_title = line[0].strip(' ')
                print(article_title, "\n")

                for g in merpy_res_nested_list:

                    if len(g) > 1:
                        with open(result_file, "a") as res_file:
                            res_file.write(article_title + "," + f_gene + "," + g[2] + "," + g[3] + "\n")
                        res_file.close()
                    else:
                        print("zero length of resultant list")
                        with open(result_file, "a") as res_file:
                            res_file.write(article_title + "," + f_gene + "," + "NA" + "," + "NA" + "\n")
                        res_file.close()
        in_file.close()
    return result_file







def perom_mer_mp(countt, input_file_name, result_file_name):

    countt = countt
    f = input_file_name
    result_file = result_file_name


    f_gene = str(f.split(".")[0])  # pick the gene name
    f_gene = f_gene.strip(' ')
    print(f, "file name")
    print(f_gene, "gene name")
    with open(f, "r") as in_file:
        lines = in_file.readlines()  # .replace('\n', '')
        # print(lines)
        for l in lines:
            line = l.split("___")
            # article_abstract = line[1].strip(' ')
            article_abstract = line[1].strip(' ')

            merpy_res_nested_list = merpy_function(article_abstract)
            # print(merpy_res_nested_list)
            article_title = line[0].strip(' ')
            print(article_title, "\n")

            for g in merpy_res_nested_list:

                if len(g) > 1:
                    with open(result_file, "a") as res_file:
                        res_file.write(article_title + "," + f_gene + "," + g[2] + "," + g[3] + "\n")
                    res_file.close()
                else:
                    print("zero length of resultant list")
                    with open(result_file, "a") as res_file:
                        res_file.write(article_title + "," + f_gene + "," + "NA" + "," + "NA" + "\n")
                    res_file.close()
    in_file.close()
    return result_file



if __name__ == "__main__":
    print("calling Mer function")
