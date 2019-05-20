#! /usr/bin/env python3

import vcf
import httplib2
import json

__author__ = 'Glueck Tobias'

class Assignment3:
    
    def __init__(self):
        ## Check if pyvcf is installed
        print("PyVCF version: %s" % vcf.VERSION)
        
        ## Call annotate_vcf_file here
        self.vcf_path = "chr16.vcf"

    def annotate_vcf_file(self):

        ## Build the connection
        h = httplib2.Http()
        headers = {'content-type': 'application/x-www-form-urlencoded'}
                
        params_pos = []  # List of variant positions
        with open(self.vcf_path) as my_vcf_fh:
            vcf_reader = vcf.Reader(my_vcf_fh)
            for counter, record in enumerate(vcf_reader):
                params_pos.append(record.CHROM + ":g." + str(record.POS) + record.REF + ">" + str(record.ALT[0]))
                
                if counter >= 899:
                    break
        
        ## Build the parameters using the list we just built
        params = 'ids=' + ",".join(params_pos) + '&hg38=true'
        
        ## Perform annotation
        res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
        annotation_result = con.decode('utf-8')
        
        self.annotation_json = json.loads(annotation_result)
        
        return self.annotation_json  ## return the data structure here
    
    def get_list_of_genes(self):
        for g in self.annotation_json:
            if "cadd" in g:
                if "genename" in g["cadd"]["gene"]:
                    return(g["cadd"]["gene"]["genename"])
    
    def get_num_variants_modifier(self):
        c = 0
        for i in self.annotation_json:
            if "snpeff" in i:
                if "putative_impact" in i["snpeff"]["ann"] and "MODIFIER" == i ["snpeff"]["ann"]["putative_impact"]:
                    c += 1
        return c 
    
    def get_num_variants_with_mutationtaster_annotation(self):
        c = 0
        for i in self.annotation_json:
            if "dbnsfp" in i:
                if "mutationtaster" in i["dbnsfp"]:
                    c += 1
        return c
        
    def get_num_variants_non_synonymous(self):
        c = 0
        for i in self.annotation_json:
            if "cadd" in i:
                if i["cadd"]["consequence"] == "NON_SYNONYMOUS":
                    c += 1
        return c
    
    def view_vcf_in_browser(self):
        print("Final URL: https://vcf.iobio.io/?species=Human&build=GRCh38")
                
    def print_summary(self):
        self.annotate_vcf_file()
        print("List of genes: " + str(self.get_list_of_genes()))
        print("Number of variants: " + str(self.get_num_variants_modifier()))
        print("Number of variants with mutations: " + str(self.get_num_variants_with_mutationtaster_annotation()))
        print("Number of non synonymous variants: " + str(self.get_num_variants_non_synonymous()))
        self.view_vcf_in_browser()

def main():
    print("Assignment 3")
    assignment3 = Assignment3()
    assignment3.print_summary()
    print("Done with assignment 3")
        
if __name__ == '__main__':
    main()