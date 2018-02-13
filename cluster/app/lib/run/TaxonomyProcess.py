import networkx as nx
from networkx.readwrite import json_graph
import json


def taxoLevels():
    taxonomy=["Domain","Phylum","Class","Order","Family","Genus","Species"]
    tindex={-1:"Root",0:"Domain",1:"Phylum",2:"Class",3:"Order",4:"Family",5:"Genus",6:"Species",7:"Sub-species"}
    return[taxonomy,tindex]

def load_abundance(fi):
    abundance=[]
    for i in open(fi):
        abundance.append(i.split('\t'))
    return abundance

#g=taxonomy_tree(load_abundance('alignment.BpErAFsqEm.matches.taxonomy.abundance.rpkm'),'/home/gustavo1/tmp/a','b','c','d')

def taxonomy_tree(abundance,filename,pipeline,analysis,dbname):
    G=nx.DiGraph()
    counts,tix=taxoLevels()
    for i in abundance:
        #i=i.split()
        taxo=i[-1].replace("\n","").split(";") #last column is the taxonomy lineage
        taxo=['R']+taxo
        
        abundance=float(i[1])/2 #first column is the number of sites (unique sites)
        matches=float(i[2])/2 #Second column is the number of matches
        rpkm=float(i[3])/2
        
        for tx in range(len(taxo)-1):
            parent=taxo[tx].replace("unknown","unknown."+taxo[tx-1]).replace("uncultured","uncultured."+taxo[tx-1])
            child=taxo[tx+1].replace("unknown","unknown."+taxo[tx]).replace("uncultured","uncultured."+taxo[tx])
            #if "unknown" in parent or "unknown" in child: break
            if not (parent,child) in G.edges():
                if not child in G.nodes():
                    G.add_node(child,matches=matches,sites=abundance,rpkm=rpkm,level=tix[tx])
                else:
                    G.node[child]['sites']+=abundance;G.node[child]['rpkm']+=rpkm; G.node[child]['matches'] +=matches;
                if not parent in G.nodes():
                    G.add_node(parent,matches=matches,sites=abundance,rpkm=rpkm,level=tix[tx-1])
                else:
                    G.node[parent]['sites'] +=abundance; G.node[parent]['rpkm']+=rpkm; G.node[parent]['matches'] +=matches;
                if not G.predecessors(child):
                    G.add_edge(parent,child)
            else:
                G.node[parent]['sites']+=abundance;G.node[parent]['rpkm']+=rpkm; G.node[parent]['matches'] +=matches;
                G.node[child]['sites'] +=abundance; G.node[child]['rpkm']+=rpkm; G.node[child]['matches'] +=matches;
    try:
        G.node['R']['rpkm']=2*G.node['R']['rpkm']
    except:
        G.add_node('R')
        G.node['R']['rpkm']=1
        G.node['R']['matches']=1
        G.node['R']['sites']=1
        G.node['R']['level']='Root'
    # now take the different levels
    #print G.node['R']['level']
    #print  G.edges('Bacteria')
    if pipeline=="matches":
        nx.write_gpickle(G,filename+"."+analysis+".abundance"+'.pk')
        tree=json_graph.tree_data(G,root='R')
        with open(filename+"."+analysis+".abundance"+'.json', 'w') as outfile:
            json.dump(tree, outfile)
    else:
        nx.write_gpickle(G,filename+"."+analysis+".abundance"+'.pk')
        tree=json_graph.tree_data(G,root='R')
        with open(filename+"."+analysis+".abundance"+'.json', 'w') as outfile:
            json.dump(tree, outfile)
    return(G)


















def metaphlan_taxonomy_tree(filename):
    with open(filename) as f:
        content = f.readlines()
    G=nx.DiGraph()
    counts,tix=taxoLevels()
    #add first node bacteria!
    for i in content[2:-1]:
        i=i.split()
        taxo=['R']+i[0].split("|")
        #print taxo
        matches=int(i[4])
        abundance=float(i[1])
        G.add_node(taxo[-1], sites=abundance, matches=matches, rpkm=abundance, level=tix[len(taxo)-2])
        for tx in range(0,len(taxo)-1):
            parent=taxo[tx]
            child=taxo[tx+1]
            G.add_edge(parent,child)
    try:
        G.node['R']['rpkm']=G.node['k__Bacteria']['rpkm']
        G.node['R']['matches']=G.node['k__Bacteria']['matches']
        G.node['R']['sites']=G.node['k__Bacteria']['sites']
        G.node['R']['level']='Root'
    except:
        G.add_node('R')
        G.node['R']['rpkm']=1
        G.node['R']['matches']=1
        G.node['R']['sites']=1
        G.node['R']['level']='Root'
        
    tree=json_graph.tree_data(G,root='R')
    with open(filename+".taxonomy.abundance.json", 'w') as outfile:
        json.dump(tree, outfile)
    nx.write_gpickle(G,filename+'.taxonomy.abundance.pk')
    return G





def mytaxa_taxonomy_tree(data,filename):
    G=nx.DiGraph()
    counts,tix=taxoLevels()
    for lineage in data:
        taxo=['R']+lineage.split(";")
        for tx in range(len(taxo)-1):
            parent=taxo[tx]
            child=taxo[tx+1]
            matches=data[lineage]['genes']
            abundance=data[lineage]['scaffold']

            #if "unknown" in parent or "unknown" in child: break
            if not (parent,child) in G.edges():
                if not child in G.nodes():
                    G.add_node(child,matches=matches,sites=abundance,rpkm=1*float(matches),level=tix[tx])
                else:
                    G.node[child]['sites']+=abundance;G.node[child]['rpkm']+=1*float(matches); G.node[child]['matches'] +=matches;
                if not parent in G.nodes():
                    G.add_node(parent,matches=matches,sites=abundance,rpkm=1*float(matches),level=tix[tx-1])
                else:
                    G.node[parent]['sites'] +=abundance; G.node[parent]['rpkm']+=1*float(matches); G.node[parent]['matches'] +=matches;
                if not G.predecessors(child):
                    G.add_edge(parent,child)
            else:
                G.node[parent]['sites']+=abundance;G.node[parent]['rpkm']+=1*float(matches); G.node[parent]['matches'] +=matches;
                G.node[child]['sites'] +=abundance; G.node[child]['rpkm']+=1*float(matches); G.node[child]['matches'] +=matches;
    G.node['R']['rpkm']=2*G.node['R']['rpkm']
    tree=json_graph.tree_data(G,root='R')
    with open(filename+".json", 'w') as outfile:
        json.dump(tree, outfile)
    nx.write_gpickle(G,filename+'.pk')
    return G












                #
