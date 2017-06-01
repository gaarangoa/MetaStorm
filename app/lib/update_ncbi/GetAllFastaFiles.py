import os
import urllib2 
import re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

inputDir="/research/gustavo1/metagenomics/databases/Genomes/all.fna/"
outDir=open("/research/gustavo1/metagenomics/databases/Genomes/BacteriaGenomesProteinSequences.fa","w")
url="ftp://ftp.ncbi.nlm.nih.gov/genomes/Bacteria/" #Bifidobacterium_longum_infantis_157F_uid62693/NC_015052.gbs"

files=os.listdir(inputDir)
count=0
flag1=0
flag2=0
record=[]
for i in files:
	print str(count) +"of"+ str(len(files))
	count+=1
	docs=os.listdir(inputDir+"/"+i)
	for j in docs:
		j=j.replace(".fna","")
		req = urllib2.Request(url+i+"/"+j+".gbk")
		try:
			response = urllib2.urlopen(req)
			the_page = response.read()
			lineage="".join(the_page.split("ORGANISM")[1].split('REFERENCE')[0].split("\n")[1:]).replace(" ","")
			flag=0
			for ix in the_page.split("\n"):
				if re.search("\/db_xref=\"GI:",ix): 
					sequence=ix.replace("/db_xref=","").replace("\"","").replace(" ","")+ "\t"		
				if re.search("\/translation=",ix):
					sequence=sequence+ix.replace(" ","").replace("/translation=","").replace("\"","")					
					flag=1
					flag2=1
				if len(ix.split())>1 and flag2==1:
					name=sequence.split()[0]+"|"+i+"|"+j+"|"+lineage
	 				record.append(SeqRecord(Seq(sequence.split()[1]),id=name))				
					#outDir.write(">"+sequence.split()[0]+"\t"+i+"\t"+j+"\t"+lineage+"\n"+"\n".join(re.findall('.'*50+'?',sequence.split()[1]))+"\n")
					#print(">"+sequence.split()[0]+"|"+i+"|"+j+"|"+lineage+"\n"+"\n".join(re.findall('.'*50+'?',sequence.split()[1]))+"\n")
					flag=0
					flag2=0
				if flag==1 and not re.search("\/",ix):
					sequence=sequence+ix.replace(" ","").replace("/translation=","").replace("\"","")
		except: 
			print("Error!" + i + j)

SeqIO.write(record,outDir,"fasta")
outDir.close()
