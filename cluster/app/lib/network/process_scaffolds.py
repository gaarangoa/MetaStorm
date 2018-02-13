import os, json
import app.lib.common.rootvar as rootvar
import app.lib.common.color as color
import app.lib.common.module as pre
import networkx as nx



pid='f2NZZKpLkHm7Cgq'

sids=['IpVBVWsXYJ2IUqk']

sdir=rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sids[0]+"/"

fi=sdir+'scaffold.fa'

scaffold={}
for line in open(fi):
    if line[0]==">":
        line=line.split()
        scaffold[line[0].split('_')[1]]={'len': int(line[1].split("_")[1]), 'reads':int(line[2].split("_")[-1])}
    

json.dump(scaffold, open(fi+".json",'w'))


fi=sdir+'pred.genes.prot.fa'

genes={}
for line in open(fi):
    if line[0]==">":
        line=line.split()
        genes[line[0].replace(">","")]={'start':int(line[2]), 'end':int(line[4]), 'strand':int(line[6]), 'scaffold':line[0].split("_")[1]}

json.dump(scaffold, open(fi+".json",'w'))





rids=['fRH6jSMue3', 'W728UFDzsk']
COLOR={}

minlen=25
iden=50
evalue=1e-20
colix=1
G={}#["scaffold_id\tscaffold_gene\tmatched_gene\tidentity\tlength\tposition\tstrand\trid\function\n"]
for rid in rids:
    ri=sdir+'pred.genes.'+rid+".matches"
    COLOR[rid]=color.rnd(colix); colix+=9
    # load reference annotation
    DBCid_description=json.load(open(rootvar.__ROOTDBS__+"/"+rid+"/dataset.description.json"))
    MetaStormCid_DBCid={line.split()[0]:line.split()[2] for line in open(rootvar.__ROOTDBS__+"/"+rid+"/func.db")}
    genes_MetaStormCid=[[line.split()[0],DBCid_description[MetaStormCid_DBCid[line.split()[1]]]['X1']] for line in open(rootvar.__ROOTDBS__+"/"+rid+"/dataset.func")]
    
    GM={}
    for i in genes_MetaStormCid:
        try:
            GM[i[0]].update(i[1])
        except:
            GM[i[0]]=[i[1]]
    
    for line in open(ri):
        line=line.strip().split("\t")
        if float(line[2])>=iden and float(line[3])>=minlen and float(line[10])<=evalue:
            si=line[0].split("_")[1]
            identity=float(line[2])
            length=float(line[3])
            position=float(line[8])+genes[line[0]]['start']
            strand=genes[line[0]]['strand']
            functions=GM[line[1]]
            
            for function in functions:
                try:
                    G[si].append([line[0], line[1], identity, length, position, strand, rid, function])
                except:
                    G[si]=[[line[0], line[1], identity, length, position, strand, rid, function]]



from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
import math
from py2cytoscape import util as cy 
   
Graph=nx.Graph()
    
for item in G:
    GeneList=G[item]
    #distances=squareform(pdist([[math.log(i[4])] for i in G[item]]))
    for i,value in enumerate(GeneList):
        for j,value2 in enumerate(GeneList[i:]):
            if j!=0: # for making the nested loop
                p=value[-1]
                q=value2[-1]
                distance=(pdist([[value[-4]],[value2[-4]]])[0]+1)/1000 # distance per 1kb
                if distance>50000: continue #distance=50000
                try:
                    #count=Graph[p][q]['score']
                    
                    Graph.node[p]['count']+=1
                    Graph.node[q]['count']+=1
                    
                    if p!=q:
                        if distance<Graph[p][q]['distance']: Graph[p][q]['distance']=distance
                        Graph.edge[p][q]['count']+=1
                except:
                    
                    Graph.add_node(p,count=1, refdb=value[-2], color=COLOR[value[-2]])
                    Graph.add_node(q,count=1, refdb=value2[-2], color=COLOR[value2[-2]])
                    
                    if p!=q:
                        if value2[-2]==value[-2]:
                            link_color=COLOR[value[-2]]
                        else:
                            link_color='#000000'
                        Graph.add_edge(p,q,distance=distance,count=1, link_color=link_color)
                    
                    #print i,j+i,value,value2,math.log(pdist([[value[-4]],[value2[-4]]])[0])


Gc=cy.from_networkx(Graph)
json.dump(Gc,open('test.json','w'))



















