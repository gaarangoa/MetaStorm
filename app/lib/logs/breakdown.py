import app.lib.common.rootvar as rootvar
import json
import os

def assembly(data):
    pid=data["pid"]
    uid=data["uid"]
    sid=data["sid"]
    rid=data["rid"]
    diri=rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/"
    #get total number of genes:
    totalGenes=0
    for i in open(diri+"pred.genes.gff"):
        if not "#" in i:
            totalGenes+=1
    
    for i in open(rootvar.__ROOTPRO__+"/"+pid+"/READS/"+sid+"trim.log"):
        if "Input Read Pairs:" in i:
            i=i.split()
            totalReads=int(i[6])
            textReads=" ".join(i)
            break
    
    taxonomy={}
    taxo=[]
    for i in rid[0]:
        #print i
        ki=i
        i=i[0]
        try:
            if i=="abcdefghij":
                file=diri+"pred.genes."+i+".matches.taxonomy.abundance.json"
                x=json.load(open(file))
                genes=0
                for ti in x['children']: genes+=ti['matches']
                taxonomy.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
                taxo.append([ki[1],int(genes), i, ki[2]])
            else:
                file=diri+"pred.genes."+i+".matches.taxonomy.abundance.rpkm"
                genes=0
                
                for ti in open(file):
                    genes+=int(ti.split()[2])
                taxo.append([ki[1],genes, i, ki[2]])
                taxonomy.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
        except:
            pass

    function={}
    func=[]
    for i in rid[1]:
        try:
            ki=i
            i=i[0]
            file=diri+"pred.genes."+i+".matches.function.genes.abundance.rpkm"
            genes=0
            for ti in open(file):
                genes+=int(ti.split()[2])
            func.append([ki[1],genes, i, ki[2]])
            function.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
        except:
            pass
    #print taxo, func
    return [taxonomy, function, taxo, func, totalGenes, textReads,data]



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
            textReads=" ".join(i)
            break
    
    #get total number of genes:
    taxonomy={}
    taxo=[]
    for i in rid[0]:
        #print i
        ki=i
        i=i[0]
        try:
            if i=="abcdefghij":
                fi=diri+"alignment."+i+".matches.taxonomy.abundance.json"
                x=json.load(open(fi))
                genes=0
                for j in x['children']: genes+=j['matches']
                taxonomy.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
                taxo.append([ki[1],genes,i, ki[2]])
            else:            
                file=diri+"alignment."+i+".matches.taxonomy.abundance.rpkm"
                if not os.path.exists(file): continue
                genes=0
                for ti in open(file):
                    genes+=int(ti.split()[2])
                taxo.append([ki[1],genes,i, ki[2]])
                taxonomy.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
        except:
            pass

    function={}
    func=[]
    for i in rid[1]:
        try:
            ki=i
            i=i[0]
            file=diri+"alignment."+i+".matches.function.genes.abundance.rpkm"
            if not os.path.exists(file): continue
            genes=0
            isgenes={}
            for ti in open(file):
                genes+=int(ti.split()[2])
            func.append([ki[1],genes,i, ki[2]])
            function.update({i:{'name':ki[1],'Ngenes':genes,'evalue':0}})
        except:
            pass    
        
    
    #print taxo, func
    return [taxonomy, function, taxo, func, totalReads, textReads]