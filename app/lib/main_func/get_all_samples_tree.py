from app.lib.run.MAIN_PROCESS import process as MP
from app.lib.run.Assembly import idbaud as idba
from werkzeug import secure_filename
import os,re
from app.lib.common import module
from app.lib.common import rootvar
import json
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
#from app.lib.run import MAIN_PROCESS as MP
from app.lib.create_project import insert_new_project as sql

main_db = rootvar.__FILEDB__

def taxonomy(data):
    pid=data["pid"]
    uid=data["uid"]
    sids=data["sid"]
    pipeline=data["pip"]
    rid=data["rid"]
    edges=[]
    FULL_MATRIX=[]
    #first see if the data set contains taxonomy, function or both annotations
    analysis="taxonomy"
    # print '\n\n\n here we goo!!!\n\n\n', pipeline
    rootvar.mkdir(rootvar.__ROOTPRO__+"/"+pid+"/"+pipeline+"/RESULTS/")
    all_samples_tree_file=rootvar.__ROOTPRO__+"/"+pid+"/"+pipeline+"/RESULTS/"+rid+".all_samples_tree.pk"
    #
    # stored_samples=0
    # if os.path.isfile(all_samples_tree_file):
    #     #print '\n\n\n if the X file has been created'
    #     x=sql.SQL(all_samples_tree_file+".db")
    #     val=x.exe("select distinct sample_name from full_matrix")
    #     stored_samples=len(val)
    # #
    x=sql.SQL(main_db)
    # TODO !! HERE the status of the sample is not being checed, it has to be checked seems that the database is being lock for some unknown reason!! 
    # sids=x.exe('select c.sample_id from (select * from samples a inner join (select * from sample_status where pip="'+str(pipeline)+'") b on a.sample_id==b.sid) c where c.project_id=="'+pid+'" and c.rid="'+rid+'"')
    #
    #
    #print '\n\n\n\n super important \n', sids
    #print '\n\n\n get all the samples from the X file'
    #   
    # if os.path.isfile(all_samples_tree_file) and stored_samples == len(sids):
    #     #print 'both have the same length'
    #     G=nx.read_gpickle(all_samples_tree_file)
    #     tree=json_graph.tree_data(G,root='R')
    #     return ["taxonomy",tree]
    #section
    #print '\n\n\n SO the file has not been created, because the matrix of abundances has not been fetched for those samples'
    nodes={}
    #print '\n\n\n So for each sample I get all the information from the sql tables. And create the tree \n\n\n\n\n\n'
    #
    for sid in sids:
        try:
            samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
            xpath=x.project(pid)[0][4]
            sample=rootvar.samples(samples[0],xpath)
            rf=rootvar.result_files(pid,analysis,pipeline,sample.id,rid)
            view=rootvar.ViewSampleResults(sample,pipeline,rid,analysis,rf)
            FULL_MATRIX+=view.all()
            Gp=nx.read_gpickle(rf.pk)
            edges+=Gp.edges()
            for node in Gp.nodes():
                if not node in nodes:
                    nodes[node]=Gp.node[node]['level']
        except:
            # IGNORE samples that don't have information
            pass
    
    x.close()
    # rootvar.full_matrix_sql(all_samples_tree_file+".db", FULL_MATRIX)
    G=nx.DiGraph()
    for i in edges:
        if not i in G.edges():
            if not i[1] in G.nodes():
                G.add_node(i[1],samples=1,level=nodes[i[1]])
            else:
                G.node[i[1]]['samples']+=1
            if not i[0] in G.nodes():
                G.add_node(i[0],samples=1,level=nodes[i[0]])
            else:
                G.node[i[0]]['samples']+=1
            if not G.predecessors(i[1]):
                G.add_edge(i[0],i[1])
        else:
            G.node[i[0]]['samples']+=1
            G.node[i[1]]['samples']+=1
    tree=json_graph.tree_data(G,root='R')
    nx.write_gpickle(G,all_samples_tree_file)
    return ["taxonomy",tree,all_samples_tree_file+".json"]

def functional(data):
    pid=data["pid"]
    uid=data["uid"]
    sids=data["sid"]
    pipeline=data["pip"]
    rid=data["rid"]
    edges=[]
    FULL_MATRIX=[]
    #first see if the data set contains taxonomy, function or both annotations
    analysis="function"
    #print rid
    #
    #
    os.system("mkdir "+rootvar.__ROOTPRO__+"/"+pid+"/"+pipeline+"/RESULTS/ >> "+rootvar.log+" 2>&1")
    all_samples_tree_file=rootvar.__ROOTPRO__+"/"+pid+"/"+pipeline+"/RESULTS/"+rid+".all_samples_tree.pk"

    log = open(rootvar.__ROOTPRO__+"/"+pid+"/"+pipeline+"/RESULTS/"+rid+".log", "w")

    #
    # if os.path.isfile(all_samples_tree_file):
    #     x=sql.SQL(all_samples_tree_file+".db")
    #     val=x.exe("select distinct sample_name from full_matrix")
    #     stored_samples=len(val)
    #
    # x=sql.SQL(main_db)
    # # load all the samples that have been finalized to run
    # sids=x.exe('select c.sample_id from (select * from samples a inner join (select * from sample_status where pip="'+str(pipeline)+'") b on a.sample_id==b.sid) c where c.project_id=="'+pid+'" and c.status="Done" and c.rid="'+rid+'"')
    # x.close()
    # if os.path.isfile(all_samples_tree_file) and stored_samples == len(sids):
    #     x=sql.SQL(all_samples_tree_file+".db")
    #     FULL_MATRIX=x.exe("select * from full_matrix")
    #     return ["function",FULL_MATRIX,all_samples_tree_file+".json"]
    # nodes={}

    x=sql.SQL(main_db)
    log.write("echo #LOG for Project ID: "+str(pid)+"\n")
    for sid in sids:
        samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
        # log.write(str(sid)+"\n")
        xpath=x.project(pid)[0][4]
        sample=rootvar.samples(samples[0],xpath)
        #print sample.name
        # log.write(str(samples[0])+"\n")
        rf=rootvar.result_files(pid,analysis,pipeline,sample.id,rid)
        view=rootvar.ViewSampleResults(sample,pipeline,rid,analysis,rf)
        FULL_MATRIX+=view.all_func()
        #print sample.name
    x.close()
    # log.write(str(FULL_MATRIX))
    #print FULL_MATRIX[0]
    #rootvar.full_matrix_function(all_samples_tree_file+".db", FULL_MATRIX)
    #print "matrix done"
    # tree=["none"]
    return ["function",FULL_MATRIX, all_samples_tree_file+".json"]





def run(data):
    rid=data['rid']
    x=sql.SQL(main_db)
    value = x.exe('select taxofile,functfile from reference where reference_id="'+rid+'"')[0]
    x.close()
    if rid=="MyTaxa" or rid=="abcdefghij":
        taxo= taxonomy(data)
        return taxo

    if value[0]!="none":
        #print 'taxonomy'
        taxo= taxonomy(data)
    if value[1]!="none":
        func= functional(data)

    if value[0]!="none" and value[1]!="none":
        return [taxo,func]
    elif value[0]!="none":
        return taxo
    elif value[1]!="none":
        return func
