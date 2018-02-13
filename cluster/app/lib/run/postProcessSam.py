# !/usr/bin/python
# for single end read
import sys

def decomposeCIGAR(CIGARstr):
    seqLen = 0
    pointer = 0
    shiftP = 0
    matchP = 0
    for i, c in enumerate(CIGARstr):
        if c == 'S' or c == 'I' or c=='D':
            shiftP += int(CIGARstr[pointer:i])
            pointer = i + 1
        elif c == 'M':
            seqLen = int(CIGARstr[pointer:i])
            shiftP += seqLen
            matchP += seqLen
            pointer = i + 1
    # fix the insert and delete shift by shiftP
    return (matchP, shiftP)

def process(filename,taxo, lens, taxodb,analysis,dbname):
    GENES={} # reads per genes dict structure id:gene -> reads number
    f = open(filename, 'r')
    fout = open(filename+'.ext', 'w')
    headerLineNum = 86
    matches=0
    for i in xrange(headerLineNum):
    	  f.readline()
    count = 0
    for line in f:
    	fields = line.split('\t')
    	if len(fields) <=5: continue;
    	count += 1
    	if fields[5] == '*':
    		a=0
    	else:
    		CIGAR = fields[5]
    		matchLen, alignLen = decomposeCIGAR(CIGAR)
    		seq = fields[9]
    		AS = fields[11].split(':')
    		XS = fields[12].split(':')
    		flag = 'uniq'
    		if AS[2] == XS[2] and XS[0] == 'XS':
    				flag = 'mult'
    		if fields[1]==16:position="\t".join([str(int(fields[4])-alignLen),fields[4]])
    		else: position="\t".join([fields[4],str(int(fields[4])+alignLen-1)])
    		identity=float(matchLen)/alignLen
    		outline=[fields[0],fields[2],position,str(identity),flag]
    		fout.write('\t'.join(outline)+'\n')
    		if(identity>0.9):
    			matches+=1
    			if fields[2] in GENES:
    				GENES[fields[2]]+=1
    			else:
    				GENES[fields[2]]=1
    # compute the gene-reads abundance
    #print matches
    outf=open(filename+".genes.abundance",'w')
    TAXO={}
    totalGenes=0
    #cnt=0
    for i in GENES:
        #cnt+=1
        #print cnt
    	totalGenes+=1
    	rpkm=(GENES[i]*1000000000)/(matches*float(lens[i]))
        #print "\t".join([i,taxo[i], str(GENES[i]), str(rpkm),"\n"])
    	outf.write("\t".join([i,taxo[i], str(GENES[i]), str(rpkm),"\n"]))
    	if taxo[i] in TAXO:
    		TAXO[taxo[i]][0]+=GENES[i]
    		TAXO[taxo[i]][1]+=rpkm
    		TAXO[taxo[i]][2]+=1
    	else:
    		TAXO[taxo[i]]=[GENES[i],rpkm,1]
    outf.close()
    #print filename
    #compute the gene-taxo abundance
    outf=open(filename+"."+analysis+".abundance",'w');
    ABN=[]
    for i in TAXO:
        item=[i,str(TAXO[i][2]),str(TAXO[i][0]),str(TAXO[i][1]),taxodb[i].split()[0],taxodb[i].split()[1]]
    	outf.write("\t".join(item+["\n"]))
        ABN.append(item)
    outf.close()

    return(ABN)
