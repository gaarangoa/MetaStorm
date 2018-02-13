import re,itertools,string,sys

def get_taxoTags(x):
	if(x=='Bacteria'):
		return({'subclass':'idae', 'order':'ales', 'suborder':'ineae', 'family':'aceae', 'subfamily':'oideae'})

def get_lineage(x):
	lineage=''
	rlineage=''
	domain=['Bacteria','Archaea','Eukaryota','Viruses']
	if sum([i in x for i in domain])==1:
		x=re.sub("\.|,|\s+|_1|","",x)
		x=x.replace('\n','').split(';')
		taxoTags=get_taxoTags('Bacteria')
		if(len(x)>=3): lineage={'domain': re.sub("\.|,|\s+|_1|","",x[0]), 'phylum':re.sub("\.|,|\s+|_1|","",x[1]), 'class':re.sub("\.|,|\s+|_1|","",x[2])}
		if(len(x)==2): lineage={'domain': re.sub("\.|,|\s+|_1|","",x[0]), 'phylum':re.sub("\.|,|\s+|_1|","",x[1]), 'class':'unknown'}
		if(len(x)==1): lineage={'domain': re.sub("\.|,|\s+|_1|","",x[0]), 'phylum':'unknown', 'class':'unknown'}
		for tag in taxoTags:
			regex=re.compile(".*("+taxoTags[tag]+")$") # Order\
			rmatch="_".join([m.group(0) for l in x for m in [regex.search(l)] if m])
			if rmatch:
				lineage[tag]=re.sub("\.|,|\s+|_1|","",rmatch)
			else:
				lineage[tag]='unknown'
		rex=";".join(x[3:])
		rex=re.sub("[A-Z](.+?)(idae|ales|ineae|aceae|oideae|eae|inae);","",rex).split(";")
		if(len(rex)>=2):
			lineage['genus']=re.sub("\.|,|\s+|_1|","",rex[0])
			lineage['species']=re.sub("\.|,|\s+|_1|","",rex[1])
		elif(len(rex)==1 and rex[0]!=""):
			lineage['genus']=re.sub("\.|,|\s+|_1|","",rex[0])
			lineage['species']='unknown'
		else:
			lineage['genus']='unknown'
			lineage['species']='unknown'
		rlineage=';'.join([lineage['domain'], lineage['phylum'], lineage['class'], lineage['order'], lineage['family'], lineage['genus'], lineage['species']])
	return([lineage,rlineage])

def get_alphabet(size):
	alpha=string.ascii_lowercase+string.ascii_uppercase+'0123456789'
	return(["".join(i) for i in itertools.product(alpha,repeat=size)])

def GetUniqueIdentifier(path,out_path,ifile,ftype,g,rid):
	g.db.execute('UPDATE reference SET status="start" WHERE reference_id="'+rid+'"')
	g.db.commit()
	print 'start'
	nsize=4
	if ftype=='taxo': nsize=4
	X={}
	Y=[]
	COUNTS={}
	uniqueID=get_alphabet(nsize)
	index=0
	for item in open(path+'/'+ifile):
		if not item: continue
		item=item.replace("\n","").split("\t")
		id=item[0]
		value=item[1]
		if ftype=='taxo': lineage=get_lineage(value)[1]
		else: lineage=value
		if lineage: Y.append([id,lineage])
		else: Y.append([id,"unknown"]); lineage="unknown"
		if not lineage in X:
			X[lineage]=[uniqueID[index],1]
			index+=1
		else:
			X[lineage][1]+=1
	outfile=open(out_path+"/dataset."+ftype,'w')
	g.db.execute('UPDATE reference SET status="middle" WHERE reference_id="'+rid+'"')
	g.db.commit()
	print 'middle'
	for i in Y:
		outfile.write(i[0]+'\t'+str(X[i[1]][0])+'\n')
	outfile.close()
	outfile=open(out_path+'/'+ftype+".db",'w')
	for i in X:
		outfile.write(str(X[i][0])+"\t"+str(X[i][1])+"\t"+i+"\n")
	outfile.close()
	print 'end'
	g.db.execute('UPDATE reference SET status="end" WHERE reference_id="'+rid+'"')
	g.db.commit()
	# compute the length file

	# create the blast reference file

	# create the bowtie reference file

	#create the diamond reference file



#ifile=sys.argv[1] # file
#ftype=sys.argv[2] # tag for taxo or function file

#GetUniqueIdentifier(ifile,ftype)



#awk '{if($_~/^>/){gsub(">","",$1); split($_,x,"[[:space:]]+"); y=x[2]; for(i=3;i<=length(x);i++){y=y"-"x[i]} print x[1]"\t"y}}' SILVA_123_SSURef_Nr99_tax_silva_trunc.fasta > taxonomy
