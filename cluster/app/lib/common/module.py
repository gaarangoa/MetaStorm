import re
import sys
import os, itertools, string
from fixed26 import Counter
from random import randint
import os.path

# for taxonomy
def load_features(dataset_taxo):
	data={}
	#print dataset_taxo
	if os.path.isfile(dataset_taxo):
		with open(dataset_taxo,'r') as f:
			for i in f:
				i=i.split()
				data[i[0]]=[i[1]]
				#try:
				#	data[i[0]].append(i[1])
				#except:
				#	data[i[0]]=[i[1]]
		return data
		print 'loading gene_id->db_id: done'
	else:
		return "none"

# for length
def load_features3(dataset_taxo):
	data={}
	#print dataset_taxo
	if os.path.isfile(dataset_taxo):
		with open(dataset_taxo,'r') as f:
			for i in f:
				i=i.split()
				data[i[0]]=i[1]
				#try:
				#	data[i[0]].append(i[1])
				#except:
				#	data[i[0]]=[i[1]]
		return data
		print 'loading gene_id->db_id: done'
	else:
		return "none"

# for function
def load_features2(dataset_taxo):
	data={}
	print dataset_taxo
	if os.path.isfile(dataset_taxo):
		with open(dataset_taxo,'r') as f:
			for i in f:
				i=i.split()
				#data[i[0]]=i[1]
				try:
					data[i[0]].append(i[1])
				except:
					data[i[0]]=[i[1]]
		return data
		print 'loading gene_id->db_id: done'
	else:
		return "none"



def load_taxodb(dataset_taxo):
	data={}
	if os.path.isfile(dataset_taxo):
		with open(dataset_taxo,'r') as f:
			for i in f:
				i=i.split()
				data[i[0]]="\t".join(i[1:])
		return data
		print 'loading taxo_id->lineage: done'
	else:
		return "none"




def gettaxo(level):
	return {
		"domain":0,
		"phylum":1,
		"class":2,
		"subclass":"idae",
		"order":"ales",
		"suborder":"ineae",
		"family":"aceae",
		"subfamily":"oideae",
		"tribe":"eae",
		"subtribe":"inae",
		"genus":-2,
		"species":-1,
		"none":1,
	}[level]

def gettype(x):
	return{
		"taxonomy":0,
		"function":1,
	}[x]

def bothTaxoFun(x):
	return{
		"cazy":2,
		"genomes":0,
		"silva":0,
		"foam":1,
		"cardAT":2,
		"cardAR":2,
	}[x]

def get_lineage(x):
	lineage=''
	domain=['Bacteria','Archaea','Eukaryota']
	if sum([i in x for i in domain])==1:
		x=x.replace('\n','').split(';')
		taxoTags={'subclass':'idae', 'order':'ales', 'suborder':'ineae', 'family':'aceae', 'subfamily':'oideae'}
		if(len(x)>=3): lineage={'domain': x[0].replace(".","").replace("_1",""), 'phylum':x[1].replace(".","").replace("_1",""), 'class':x[2].replace(".","").replace("_1","")}
		if(len(x)==2): lineage={'domain': x[0].replace(".","").replace("_1",""), 'phylum':x[1].replace(".","").replace("_1",""), 'class':''}
		if(len(x)==1): lineage={'domain': x[0].replace(".","").replace("_1",""), 'phylum':'', 'class':''}
		for tag in taxoTags:
			regex=re.compile(".*("+taxoTags[tag]+")$") # Order\
			rmatch="_".join([m.group(0) for l in x for m in [regex.search(l)] if m])
			lineage[tag]=rmatch.replace(".","").replace("_1","")
		rex=";".join(x[3:])
		rex=re.sub("[A-Z](.+?)(idae|ales|ineae|aceae|oideae|eae|inae);","",rex).split(";")
		if(len(rex)==2):
			lineage['genus']=rex[0].replace(".","").replace("_1","")
			lineage['species']=rex[1].replace(".","").replace("_1","")
		else:
			lineage['genus']=rex[0].replace(".","").replace("_1","")
			lineage['species']=''
	return(lineage)

def openMain(infile,db,samples,level,evalue,process):
	fresu='scaffold.diamond.'+db+'.matches.m8.reduced'
	data=[]
	corrupted_data=[]
	process=gettype(process)
	#outf=open(infile+"/results/"+db+"."+samples+"."+str(level)+"."+evalue+"."+process+".csv",'w')
	lens={}

	for sample in samples.split("*"):
		n=1
		for k in open(infile+'/'+sample+'/'+fresu):
			i=k.split();
			if float(i[-2])<float(evalue):
				lineage=get_lineage(i[6])
				if lineage != '':
					rlineage=[lineage['domain'], lineage['phylum'], lineage['class'], lineage['order'], lineage['family'], lineage['genus'], lineage['species']]
					if lineage[level]!='':
						data.append(i[0:3]+[lineage[level]]+[i[7].split("***")[-1]]+[i[8]]+[i[5]]+[rlineage])
				#else:
					#data.append(i[0:3]+['unknown']+[i[7].split("***")[-1]]+[i[8]]+[i[5]]+[rlineage])
				n+=1;
		lens[sample]=n

	taxo={}
	count=1
	for item in data:
		key=item[0]+"*"+item[1]+"*"+"_".join(item[2].split('_')[0:2])
		if not key in taxo:
			taxo[key]=[[item[3]],[item[4]]]
		else:
			count+=1
			taxo[key][0].append(item[3])
			taxo[key][1].append(item[4])

	# if the reference contains both taxonomy and functional annotation make this step:
	Btable2={}
	if(bothTaxoFun(db)==2):
		Btable={}
		for scaffold in taxo:
			Item=taxo[scaffold][0]
			numItems=len(Item)
			countItems=Counter(Item)
			countItems2=Counter(taxo[scaffold][1])
			for taxoI in countItems:
				# frequency, times, total, functional
				freq=100*float(countItems[taxoI])/float(numItems)
				#of.write("\t".join(scaffold.split('*')+[str(freq),str(countItems[taxoI]),str(float(numItems))])+"\n")
				if not scaffold in Btable:
					Btable[scaffold]=[str(freq),str(countItems[taxoI]),str(float(numItems)),taxoI.replace("group",""),countItems2]
				elif float(Btable[scaffold][0])<freq:
					Btable[scaffold]=[str(freq),str(countItems[taxoI]),str(float(numItems)),taxoI.replace("group",""),countItems2]

		Btable2={}
		for i in Btable:
			for j in Btable[i][4]:
				for k in list(set(j.split("_"))):
					out=i.split("*")+Btable[i][0:-1]+[k]
					key=out[0]+"*"+out[1]+"*"+out[6]+"*"+out[7]
					if key in Btable2:
						Btable2[key]=Btable2[key]+Btable[i][4][j]
					else:
						Btable2[key]=Btable[i][4][j]

		outf=open(infile+"/results/"+db+"SAMPLESall"+"LEVEL"+str(level)+"EVALUE"+evalue+".csv",'w')
		for i in Btable2:
			outf.write(i.replace("*","\t")+"\t"+str(Btable2[i])+"\n")

		outf.close()

	#make matrix samples/function

	svector={}
	for scaffold in taxo:
		Item=taxo[scaffold][process]
		numItems=len(Item)
		countItems=Counter(Item)
		for taxoI in countItems:
			for it in taxoI.split("_"):
				key=scaffold.split("*")[0]+"*"+it
				if not key in svector:
					svector[key]=1
				else:
					svector[key]=svector[key]+1


	sum={}
	for i in svector:
		key=i.split("*")[0]
		if key in sum:
			sum[key]=sum[key]+svector[i]
		else:
			sum[key]=svector[i]

	maxN=max(sum.values())

	outf=open(infile+"/results/"+db+"SAMPLESall"+"LEVEL"+str(level)+"EVALUE"+evalue+"TYPE"+str(process)+".all.csv",'w')

	vector=[]
	vector.append([])
	vector.append([])
	vector.append([])

	for key in svector:
		#key=key.replace(",","_")
		keyin=key.split('*')[0]
		if len(key.split('*'))==2 and not key.split('*')[1].replace('.','').isdigit():
			outf.write(key.replace('*','\t')+"\t"+str(svector[key])+"\t"+str(svector[key]*maxN/float(sum[keyin]))+"\n")
			vector[0].append(key.split("*")[0])
			vector[1].append(key.split("*")[1])
			vector[2].append(svector[key]*maxN/float(sum[keyin]))
		else:
			print 'error '+key

	outf.close()

	sample=set(vector[0])
	taxoT=set(vector[1])
	dataMatrix=[];
	#outf=open('/research/gustavo1/metagenomics/assembly/IDBA_UD/total/'+db+'.'+str(wtype)+'.all','w')
	#outf.write("Sample,"+"\t".join(sample).replace(",","_").replace("\t",",")+"\n")
	for j in taxoT:
		tx=[]
		for i in sample:
			if i+"*"+j in svector:
				tx.append(str(svector[i+"*"+j]*maxN/float(sum[i])))
			else:
				tx.append('0')
		dataMatrix.append(tx)
		#outf.write(j.replace(",","_")+","+",".join(tx)+"\n")

	#outf.close()

	import sys, numpy, scipy
	import scipy.cluster.hierarchy as hier
	import scipy.spatial.distance as dist

	dataMatrix = numpy.array(dataMatrix)
	distanceMatrix = dist.pdist(dataMatrix,'euclidean')
	distanceSquareMatrix = dist.squareform(distanceMatrix)

	linkageMatrix = hier.linkage(distanceMatrix, method='average')
	heatmapOrder = hier.leaves_list(linkageMatrix)

	orderedDataMatrix = dataMatrix[heatmapOrder,:]
	rowHeaders = numpy.array(list(taxoT))
	taxoT = rowHeaders[heatmapOrder]

	outf=open(infile+"/results/"+db+"SAMPLESall"+"LEVEL"+str(level)+"EVALUE"+evalue+"TYPE"+str(process)+".matrix.csv",'w')
	outf.write("Sample,"+"\t".join(sample).replace(",","_").replace("\t",",")+"\n")

	j=0
	matrix=[["Sample"]+"\t".join(sample).replace(",","_").split()]
	for i in orderedDataMatrix:
		outf.write(taxoT[j].replace(",","_")+","+",".join(i)+"\n")
		matrix.append([taxoT[j].replace(",","_")]+list(i))
		j+=1

	outf.close()
	#print(matrix)
	return(matrix)

def valInput(infile,db,samples,level,evalue,process):
	level=gettaxo(level)
	process=gettype(process)
	if os.path.isfile(infile+"/results/"+db+"SAMPLESall"+"LEVEL"+str(level)+"EVALUE"+evalue+"TYPE"+str(process)+".matrix.csv")==True:
		return(True)
	else:
		return(False)


def processSoft(infile,db,samples,level,evalue,process):
	level=gettaxo(level)
	process=gettype(process)
	f=open(infile+"/results/"+db+"SAMPLESall"+"LEVEL"+str(level)+"EVALUE"+evalue+"TYPE"+str(process)+".matrix.csv")
		#f=open("/home/gustavo/Dropbox/PhDProjects/metagenomics/javaScript/DisplayColorMatrix/HeatMap/Files/test")
	matrix=[]
	for i in f:
		#print i
		matrix.append(i.split(","))
	return(matrix)


def taxonomy(rootdir):
	file =  rootdir+'/A1/scaffold.diamond.genomes.matches.m8.reduced'
	for i in open(file):
		full_taxo=i.split()
	return rootdir;
