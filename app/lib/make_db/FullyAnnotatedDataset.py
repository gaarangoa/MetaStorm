import os,sys
import urllib2
import re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

def FullyAnnotatedDataset(fastaf,taxof,funcf,fastaO):
	taxo={}
	for i in taxof:
		i=i.replace("\n","").split("\t")
		taxo[i[0]]=i[1]

	func={}
	for i in funcf:
		i=i.replace("\n","").split("\t")
		func[i[0]]=i[1]

	pFasta=[]
	for record in SeqIO.parse(fastaf,"fasta"):
		id=record.id+"|"+taxo[record.id]+"|"+func[record.id]
		pFasta.append(SeqRecord(record.seq,id=id, name=id,description=''))

	SeqIO.write(pFasta,fastaO,"fasta")
	fastaO.close()

fastaf=open(sys.argv[1])
taxof=open(sys.argv[2])
funcf=open(sys.argv[3])
fastaO=open(sys.argv[4],'w')

FullyAnnotatedDataset(fastaf,taxof,funcf,fastaO)
