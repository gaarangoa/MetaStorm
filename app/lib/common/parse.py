import app.lib.common.rootvar as root
import os



def parse_blast(filename,taxo, lens, taxodb,analysis,dbname, silvafile, good_reads):
    GENES={} # reads per genes dict structure id:gene -> reads number
    f = open(filename, 'r')
    matches=0 #total number of mapped genes
    eval=1e-10 # 
    iden=90 #
    mlen=25 #
    #
    for line in f:
        line=line.split()
        if float(line[2])>=iden and float(line[3])>=mlen and float(line[10])<=eval:
            gene=line[1]
            matches+=1
            try:
                GENES[gene]+=1
            except:
                GENES[gene]=1

    # compute the gene-reads abundance
    #print matches
    lreads=100
    avg_reads_length=1432
    TAXO={}
    totalGenes=0
    #cnt=0
    #
    outf=open(filename+"."+analysis+".genes.abundance.rpkm",'w');
    root.flog('mode: Normalization by RPKM')
    for i in GENES:
        totalGenes+=1
        #rpkm=((GENES[i]*lreads)/float(lens[i]))/(matches*lreads/float(avg_reads_length))
        rpkm=(GENES[i]*1000000000)/(good_reads*float(lens[i]))
        outf.write("\t".join([i,taxo[i], str(GENES[i]), str(rpkm), str(lens[i]), "\n"]))
        if taxo[i] in TAXO:
            TAXO[taxo[i]][0]+=GENES[i]
            TAXO[taxo[i]][1]+=rpkm
            TAXO[taxo[i]][2]+=1
        else:
            TAXO[taxo[i]]=[GENES[i],rpkm,1]
    outf.close()
    #print filename
    #compute the gene-taxo abundance
    #print TAXO
    outf=open(filename+"."+analysis+".abundance.rpkm",'w');
    ABN=[]
    for i in TAXO:
        item=[i,str(TAXO[i][2]),str(TAXO[i][0]),str(TAXO[i][1]),taxodb[i].split()[0],taxodb[i].split()[1]]
        outf.write("\t".join(item+["\n"]))
        ABN.append(item)
    outf.close()
    OUT1=ABN
    #
    if analysis=="function":
        outf=open(filename+"."+analysis+".genes.abundance.16s",'w');
        root.flog('mode: Normalization by 16s rRNA abundance')
        N16s=0
        L16s=1432
        for line in open(silvafile):
            line=line.split()
            N16s+=float(line[2])
        #
        TAXO={}
        for i in GENES:
            #cnt+=1
            #print cnt
            totalGenes+=1
            rpkm=((GENES[i]*lreads)/float(lens[i]))/(N16s*lreads/float(L16s))
            #rpkm=(GENES[i]*1000000000)/(matches*float(lens[i]))
            #print "\t".join([i,taxo[i], str(GENES[i]), str(rpkm),"\n"])
            outf.write("\t".join([i,taxo[i], str(GENES[i]), str(rpkm), str(lens[i]),"\n"]))
            if taxo[i] in TAXO:
                TAXO[taxo[i]][0]+=GENES[i]
                TAXO[taxo[i]][1]+=rpkm
                TAXO[taxo[i]][2]+=1
            else:
                TAXO[taxo[i]]=[GENES[i],rpkm,1]
        outf.close()
        outf=open(filename+"."+analysis+".abundance.16s",'w');
        ABN=[]
        for i in TAXO:
            item=[i,str(TAXO[i][2]),str(TAXO[i][0]),str(TAXO[i][1]),taxodb[i].split()[0],taxodb[i].split()[1]]
            outf.write("\t".join(item+["\n"]))
            ABN.append(item)
        outf.close()
        OUT2=ABN
    if analysis=="function":
        return({'rpkm':OUT1, '16s':OUT2})
    else:
        return OUT1


# parse files from paired end reads

def compute_rpkm(C,N,L):
    # C: #reads mapped to a gene
    # N: total number of raw reads in the sample (after quality filtering)
    # L: length of the gene
    
    return (1000000000*float(C))/(float(N)*float(L))
    

def parse_sam(input,db, good_reads):
    root.flog('processing sam file')
    Genes={}
    flags={'83':1,'99':1,'73':1,'137':1,'89':1,'153':1}
    for line in open(input):
        try:
            if int(line.split("XM:i:")[1].split()[0]) < 1: #make sure that the sequence is properly aligned. The output only contains 
                line =  line.split()
                try:
                    Genes[line[2]]+=flags[line[1]]
                except:
                    try:
                        Genes[line[2]]=flags[line[1]]
                    except:
                        pass
        except:
            pass
    
    fo=open(input+'.taxonomy.abundance.genes.rpkm','w')
    taxo_id_ab={}
    for gene in Genes:
        rpkm=compute_rpkm(Genes[gene], good_reads, db.len[gene])
        fo.write("\t".join([gene, str(db.taxo[gene]), str(Genes[gene]), str(rpkm), str(db.len[gene])])+"\n")
        try:
            taxo_id_ab[db.taxo[gene]][0]+=Genes[gene] # put in the taxonomy ID the total number of reads that contains this taxonomy
            taxo_id_ab[db.taxo[gene]][1]+=rpkm
            taxo_id_ab[db.taxo[gene]][2]+=1
        except:
            taxo_id_ab[db.taxo[gene]]=[Genes[gene],rpkm,1] # number of reads in the gene, rpkm, and unique genes in the taxonomy category
    
    fo.close()
    
    fo=open(input+'.taxonomy.abundance.rpkm','w')
    ABN=[]
    for id in taxo_id_ab:
        ABN.append([id,str(taxo_id_ab[id][2]),str(taxo_id_ab[id][0]),str(taxo_id_ab[id][1]),db.taxodb[id].split()[0],db.taxodb[id].split()[1]]) # [category, unique_genes, number of reads, rpkm, lineage]
        fo.write("\t".join([id,str(taxo_id_ab[id][2]),str(taxo_id_ab[id][0]),str(taxo_id_ab[id][1]), db.taxodb[id].split()[0], db.taxodb[id].split()[1]])+"\n")
    fo.close()
    root.flog('taxonomy abundance: done')
    return ABN



def parse_diamond_blastx(input, db, good_reads):
    root.flog('processing blastx from DIAMOND')
    Genes={}
    eval=1e-5
    iden=90
    mlen=25
    for line in open(input):
        i=line.split()
        try:
            if float(i[2])>=iden and float(i[3])>=mlen and float(i[10])<=eval:
                Genes[i[1]]+=1
        except:
            if float(i[2])>=iden and float(i[3])>=mlen and float(i[10])<=eval:
                Genes[i[1]]=1
    fo=open(input+'.function.genes.abundance','w')
    for i in Genes:
        fo.write(i+'\t'+str(Genes[i])+str([db.len[i]])+'\n')
    fo.close()
    func_id_ab={}
    for gene in Genes:
        try:
            func_id_ab[db.func[gene]]+=Genes[gene] # put in the function ID the total number of reads that contains this category
        except:
            func_id_ab[db.func[gene]]=Genes[gene]
    fo=open(input+'.function.abundance','w')
    ABN=[]
    for id in func_id_ab:
        ABN.append([id,str(func_id_ab[id]),str(func_id_ab[id]),str(func_id_ab[id]),db.funcdb[id].split()[0],db.funcdb[id].split()[1]])
        fo.write("\t".join([id,str(func_id_ab[id]),db.funcdb[id].split()[1]])+"\n")
    fo.close()
    root.flog('taxonomy abundance: done')
    return ABN



























#
