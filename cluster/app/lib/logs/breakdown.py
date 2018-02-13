import app.lib.common.rootvar as rootvar

def assembly(data):
    pid=data["pid"]
    uid=data["uid"]
    sid=data["sid"]
    rid=data["rid"]
    diri=rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/"
    #get total number of genes:
    totalGenes=0
    for i in open(diri+"pred.genes.nucl.fa"):
        if ">" in i:
            totalGenes+=1

    taxonomy={}
    taxo=[]
    for i in rid[0]:
        #print i
        ki=i
        i=i[0]

        if i=="MyTaxa":
            file=diri+"pred.genes."+i+".input.pt"
            genes=open(file).readlines()
            evalue=[j.split()[-2] for j in genes]

            file=diri+"pred.genes."+i+".input.genecounts"
            genes=open(file).readlines()
            counts=sum([int(j.split()[1]) for j in genes])
            taxo.append([ki[1],counts])
            taxonomy.update({i:{'name':ki[1],'Ngenes':int(counts),'evalue':evalue}})
        elif i=="abcdefghij":
            file=diri+"pred.genes."+i+".matches"
            genes=open(file).readlines()[-1].split()[-1]
            taxonomy.update({i:{'name':ki[1],'Ngenes':int(genes),'evalue':0}})
            taxo.append([ki[1],int(genes)])
        else:
            file=diri+"pred.genes."+i+".matches"
            genes=open(file).readlines()
            evalue=[j.split()[-2] for j in genes]
            taxo.append([ki[1],len(genes)])
            taxonomy.update({i:{'name':ki[1],'Ngenes':int(len(genes)),'evalue':evalue}})

    function={}
    func=[]
    for i in rid[1]:
        ki=i
        i=i[0]
        file=diri+"pred.genes."+i+".matches"
        genes=open(file).readlines()
        evalue=[j.split()[-2] for j in genes]
        func.append([ki[1],len(genes)])
        function.update({i:{'name':ki[1],'Ngenes':int(len(genes)),'evalue':evalue}})
    #print taxo, func
    return [taxonomy, function, taxo, func, totalGenes]



def matches(data):
    pid=data["pid"]
    uid=data["uid"]
    sid=data["sid"]
    rid=data["rid"]
    diri=rootvar.__ROOTPRO__+"/"+pid+"/matches/"+sid+"/"
    
    for i in open(rootvar.__ROOTPRO__+"/"+pid+"/READS/"+sid+"trim.log"):
        if "Input Read Pairs:" in i:
            i=i.split()
            totalReads=int(i[6])
            break
    
    #get total number of genes:
    taxonomy={}
    taxo=[]
    for i in rid[0]:
        #print i
        ki=i
        i=i[0]
        
        if i=="abcdefghij":
            file=diri+"alignment."+i+".matches"
            genes=open(file).readlines()[-1].split()[-1]
            taxonomy.update({i:{'name':ki[1],'Ngenes':int(genes),'evalue':0}})
            taxo.append([ki[1],int(genes)/2])
        else:            
            file=diri+"alignment."+i+".matches.taxonomy.abundance.rpkm"
            genes=0
            for i in open(file):
                genes+=int(i.split()[2])
            taxo.append([ki[1],genes])
            taxonomy.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})

    function={}
    func=[]
    for i in rid[1]:
        ki=i
        i=i[0]
        file=diri+"alignment."+i+".matches.function.abundance.rpkm"
        genes=0
        for i in open(file):
            genes+=int(i.split()[2])
        func.append([ki[1],genes])
        function.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
    
        
    
    #print taxo, func
    return [taxonomy, function, taxo, func, totalReads]