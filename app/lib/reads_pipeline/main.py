import functions as fn
import os

#This pipeline is designed ONLY for amplicon 16s rRNA sequencing

m1="/research/gustavo1/Dropbox/PhDProjects/metagenomics/Xiao/rawreads/"#S2_R1.fastq"
samples=[['S1',m1+'S1_R1.fastq',m1+'S1_R2.fastq'],['S2',m1+'S2_R1.fastq',m1+'S2_R2.fastq']]

root="/research/gustavo1/Dropbox/PhDProjects/metagenomics/Side_pipeline/test/"

out=root+"/samples/"
fn.mkdir(out)
                                                                                                                       
# combine reads from all samples
samples_to_combine=[out+"/"+i[0]+"/seqs.fna" for i in samples]

fn.mkdir(root+"/combined/")
analysis=root+"/analysis/"
fn.mkdir(root+"/analysis/")


combined_fasta=root+"/combined/combined.fna"
os.system("cat "+' '.join(samples_to_combine)+" > "+combined_fasta)

cmd=' '.join(["pick_open_reference_otus.py -f -i ", combined_fasta, ' -o ', analysis])
os.system(cmd)







cmd=' '.join(['biom summarize-table -i ', analysis+"/otu_table_mc2_w_tax.biom > ", analysis+"/otu_table_mc2_w_tax.biom.summary"]) 
os.system(cmd)

for i in open(analysis+"/otu_table_mc2_w_tax.biom.summary"):
	if "Min: " in i:
		depth=int(float(i.split()[1]))


cmd=' '.join(["multiple_rarefactions.py",  " -i ", analysis+"/otu_table_mc2_w_tax.biom" , ' --lineages_included -m ', str(depth)," -x ", str(depth), "-s 1 -n 1	 ", ' -o ', analysis+"/rarefied_otu_tables/"])
os.system(cmd)

cmd=' '.join(["summarize_taxa_through_plots.py -f -i ", analysis+"/rarefied_otu_tables/rarefaction_"+str(depth)+"_0.biom", ' -o ', analysis+"/taxa_summary/"])
os.system(cmd)

cmd=' '.join(["summarize_taxa.py -L 7 -i ", analysis+"/rarefied_otu_tables/rarefaction_"+str(depth)+"_0.biom", ' -o ', analysis+"/taxa_summary/"])
os.system(cmd)

cmd=' '.join(["biom convert	-i ", analysis+"/rarefied_otu_tables/rarefaction_"+str(depth)+"_0.biom", ' -o ', analysis+"/rarefied_otu_tables/rarefaction_"+str(depth)+"_0.tsv --to-tsv"])
os.system(cmd)




























