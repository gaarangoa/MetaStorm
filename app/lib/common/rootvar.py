import sys, os
from subprocess import call
from app.lib.common.module import load_features
from app.lib.common.module import load_taxodb
from random import randrange, seed
import string
import networkx as nx
import sqlite3 as sql
import operator
import math
import json



#******************************************************************************
# BASIC CONSTANTS
#******************************************************************************
__root_dir__="/src/"
__ROOTM__=__root_dir__
__FILEDB__=__root_dir__+"/SQL/projects.db"
__ROOTEXEDIR__=__root_dir__+"/Files/bin/"
__ROOTPRO__=__root_dir__+"/Files/PROJECTS/"
__ROOTDBS__=__root_dir__+"/Files/REFERENCE/"
__ROOTDBSF__=__root_dir__+"/Files/REFERENCE_FORMAT/"
__TAXOLEVELS__=["Domain","Phylum","Class","Order","Family","Genus","Species"]
log=__root_dir__+"/Files/PROJECTS/debug.log"
p="64"
#******************************************************************************
# BASIC FUNCTIONS
#******************************************************************************

def tsv2json(fi,delimiter):
	data={}
	with open(fi+".json", 'w') as outfile,open(fi,"r") as f:
		for line in f:
		   sp=line.strip().split(delimiter)
		   data[sp[0]]={'X'+str(ix):i for ix,i in enumerate(sp)}
		json.dump(data, outfile)
	return data

def validate_session():
	a=1

def flog(status):
	fo=open(log,'w')
	fo.write(status+"\n")
	fo.close()


def isdir(direc):
    try:
        if os.path.getsize(direc) > 0:
            return True
        else:
            return False
    except:
        return False


def v2m(X,filters,index, minA): # from a vector x,y,value create an square matrix
	A={}
	#x=list(set([str(i[0]) for i in X]))
	#y=list(set([str(i[1]) for i in X]))

	#print len(x),len(y)
	x=[]
	y=[]
	A=nx.DiGraph()
	for i in X:
		#if i[index+2]>=0:
		A.add_edge(i[0],i[1],A=i[index+2])
		x.append(i[0])
		y.append(i[1])
	x=list(set(x))
	y=list(set(y))
	#print "graph created"
	B=[["samples"]+y]
	N=[["samples"]+y]
	edges=A.edges(); samples = {i:True for i in filters}
	#print len(edges)
    #
	for ix in x:
		item=[ix]
		ntem=[ix]
		#print ix
		if ix in filters:
			for iy in y:
				try:
					value=A[ix][iy]["A"]
					ntem.append(value)
					# item.append(math.log(value+0.001,2))
				except:
					# item.append(0)
					ntem.append(0)
			# B.append(item)
			N.append(ntem)
	#print "matrix created"
	return B,N


def filedb():
    return('/home/raid/www/MetaStorm/main/SQL/projects.db')


def rootpath():
    return("/home/raid/www/MetaStorm/main/Files/")

def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def get_alphabet(size):
    seed()
    alpha=string.ascii_lowercase+string.ascii_uppercase+'0123456789'
    uniqueID=''
    for i in range(size):
    	uniqueID+=alpha[randrange(0,62)]
    return(uniqueID)

def updateStatus(x,projectid,sampleid,message):
    x.exe('update project_status set status="'+message+'" where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    x.commit()

def checkStatusSampleRun(x,sid,process):
    value=x.exe('select 1 from sample_run where sample_id="'+sid+'" and process="'+process+'"')
    if len(value)==0:
        #print sid,process
        x.insert("sample_run",(sid,process))
        x.commit()
        return False
    else:
        return True


def full_matrix_sql(file,data):

    try:
        os.system("rm "+file+">>"+log+" 2>&1")
    except:
        pass
    conn=sql.connect(file)
    c=conn.cursor()
    c.execute('''CREATE TABLE full_matrix (sample_name varchar[50], level varchar[20], name varchar[100], sites real, matches real, rpkm real)''')
    c.executemany('INSERT INTO full_matrix VALUES (?,?,?,?,?,?)', data)
    conn.commit()
    conn.close()

def full_matrix_function(file,data):
    # samplename,functionname, relative abundance, sites
    os.system("rm "+file+">>"+log+" 2>&1")
    conn=sql.connect(file)
    c=conn.cursor()
    c.execute('''CREATE TABLE full_matrix (sample_name varchar[50], name varchar[20], abundance real, matches real, 16s real)''')
    c.executemany('INSERT INTO full_matrix VALUES (?,?,?,?,?)', data)
    conn.commit()
    conn.close()

def get_matrix_level(data,level):
    pid=data["pid"]
    uid=data["uid"]
    sids=data["sid"]
    pipeline=data["pip"]
    rid=data["rid"]

    file=__ROOTPRO__+"/"+pid+"/"+pipeline+"/RESULTS/"+rid+".all_samples_tree.pk.db"
    conn=sql.connect(file)
    c=conn.cursor()
    value = c.execute('SELECT sample_name, name, rpkm, matches  from full_matrix where level="'+level+'"').fetchall()
    conn.close()

    '''xhash={}
    yhash={}
    ix=0
    iy=0
    realValue=[]
    for item in value:
        if not item[0] in xhash:
            xhash[item[0]]=ix
            ix+=1
        if not item[1] in yhash:
            yhash[item[1]]=iy
            iy+=1
        realValue.append([xhash[item[0]],yhash[item[1]],item[2]])

    xlabs = [i[0] for i in sorted(xhash.items(), key=operator.itemgetter(1))]
    ylabs = [i[0] for i in sorted(yhash.items(), key=operator.itemgetter(1))]

    return([realValue,xlabs,ylabs])'''
    return value

import numpy as np

def get_matrix_level_childs(x,data):
    value=[]
    for i in data:
        value+=x.c.execute('SELECT sample_name, name, rpkm from full_matrix where name="'+i+'"')

    '''xhash={}
    yhash={}
    ix=0
    iy=0
    realValue=[]
    quantity=[]
    for item in value:
        if not item[0] in xhash:
            xhash[item[0]]=ix
            ix+=1
        if not item[1] in yhash:
            yhash[item[1]]=iy
            iy+=1
        realValue.append([xhash[item[0]],yhash[item[1]],item[2]])
        quantity.append(item[2])

    xlabs = [i[0] for i in sorted(xhash.items(), key=operator.itemgetter(1))]
    ylabs = [i[0] for i in sorted(yhash.items(), key=operator.itemgetter(1))]
    #print quantity
    #print np.median(quantity)
    return([realValue,xlabs,ylabs,np.median(quantity), max(quantity)])'''
    return(value)










class test:
    def __init__(self):
        self.a="x"
        self.b=os.system("ls -lstgh")




#******************************************************************************
# BASIC CLASES
#******************************************************************************



def mt_get_taxa(T):
    lineage=["superkingdom","phylum","class","order","family","genus","species"]
    taxa=[]
    for i in lineage:
        try:
            taxa.append(T.split("<"+i+">")[1].split(";")[0])
        except:
            a=1
    return ";".join(taxa)

class mytaxa:
    def __init__(self,sample,db):
        self.exe=__ROOTEXEDIR__+"/MyTaxa"
        self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
        self.output=self.path+"/pred.genes"
    def pre(self):
        os.system(''' awk '{if($_~/^>/){split($1,x,"_"); print x[1]"_"x[2]"|"x[3]}else{print}}' ''' +self.output+'.prot.fa > ' + self.output+".prot.mytaxa.fa")
    def align(self):
        os.system(__ROOTEXEDIR__+"/diamond blastp --evalue 1e-20 --id 60 -k 5 -q "+self.output+".prot.mytaxa.fa -d "+__ROOTDBS__+"/ryaetguxun/AllGenomes.faa.dmnd -a"+self.output+".MyTaxa.matches")
    def postd(self):
        os.system(__ROOTEXEDIR__+"/diamond view -a "+self.output+".MyTaxa.matches.daa -o "+self.output+".MyTaxa.align -f tab")
    def mpre(self):
        os.system(''' awk '{split($1,x,"|"); split($2,z,"|"); print $_"\t"x[1]"\t"x[2]"\t"z[2]}' ''' + self.output+".MyTaxa.align > "+ self.output+".MyTaxa.input")
    def run(self):
        data={}
        for i in open(self.output+".MyTaxa.input"):
            key=i.split("|")[0]
            key2=i.split()[0].split("|")[1]
            try:
                data[key][key2].append(i)
            except:
                try:
                    data[key].update({key2:[i]})
                except:
                    data[key]={key2:[i]}

        fo=open(self.output+".MyTaxa.input.pt",'w')
        fo2=open(self.output+".MyTaxa.input.pt.ids",'w')
        fo3=open(self.output+".MyTaxa.input.genecounts",'w')
        D={}
        for key in data:
            #print len(data[key])
            if len(data[key])>1:
                fo3.write(key+"\t"+str(len(data[key]))+"\n")
                for scf in data[key]:
                    if len(data[key][scf])>=5:
                        try:
                            D[key].update({scf:data[key][scf]})
                        except:
                            D[key]={scf:data[key][scf]}
        fo3.close()
        #IMPORTANT I need to write a file with the actual IDS to recover if is the case later.
        for key in D:
            if len(D[key])>1:
                ixk=1;
                for key2 in D[key]:
                    for item in D[key][key2]:
                        item=item.split()
                        item[13]=str(ixk)
                        fo.write("\t".join(item)+"\n")
                        fo2.write(item[0]+"\t"+item[13]+"\t"+str(ixk)+"\n")
                    ixk+=1
        fo.close()
        fo2.close()
        os.system(__ROOTEXEDIR__+"/MyTaxa " + self.output+".MyTaxa.input.pt " + self.output+".MyTaxa.output 0.5")
        os.system(''' awk '{x=$_; getline; print x"\t"$_}' ''' +  self.output+".MyTaxa.output > " + self.output+".MyTaxa.out")
    def postM(self):
        #load genecounts
        GC={}
        for i in open(self.output+".MyTaxa.input.genecounts"):
            i=i.split()
            GC[i[0]]=int(i[1])
        #load predictions:
        data={}
        for i in open(self.output+".MyTaxa.out"):
            i=i.split("\t")
            key=mt_get_taxa(i[4].replace("\n",""))
            try:
                data[key]['genes']+=GC[i[0]]
                data[key]['scaffold']+=1
                data[key]['Clen']+=int(i[3])
            except:
                if not i[3]=='NA':
                    data[key]={'genes':GC[i[0]], 'scaffold':1, 'Clen':int(i[3])}
        return data



class program:
    def __init__(self,program,sample,db):
        if program=='bowtie2':
            self.exe=__ROOTEXEDIR__+"/bowtie2"
            self.options="--sensitive-local --no-unal -p "+p
            self.program=program
            self.sample=sample
            self.db=db
            self.sam=sample.matchesDir+"alignment."+db.name+".sam"
            self.log=">>"+sample.matchesDir+"alignment."+db.name+".log 2>&1"
            self.cmd=" ".join([self.exe,"-x", db.bowtie, "-U", sample.ureads, self.options,"-S", self.sam, self.log])
        elif program=='flash':
            self.exe=__ROOTEXEDIR__+"flash"
            self.options="--allow-outies -M 100bp"
            self.program=program
            self.sample=sample
            self.out=sample.matchesDir
            self.log=">>"+sample.matchesDir+"flash.log 2>&1"
            self.cmd=" ".join([self.exe,'--allow-outies -M 100','-d', str(self.out), '-o', "flash", str(self.sample.reads1), str(self.sample.reads2), self.log  ])
        elif program=='fq2fa':
            self.exe=__ROOTEXEDIR__+"fq2fa"
            self.options="--merge --filter"
            self.program=program
            self.sample=sample
            self.db=db
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.out=self.path+"/reads.fa"
            self.cmd=" ".join([self.exe,self.options, sample.reads1, sample.reads2, self.out])
            mkdir(self.path)
        elif program=='idba_ud':
            self.exe=__ROOTEXEDIR__+"idba_ud"
            self.options="--num_threads "+p
            self.program=program
            self.sample=sample
            self.db=db
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.input=self.path+"/reads.fa"
            self.out=self.path+"/scaffold.fa"
            self.cmd=" ".join([self.exe,self.options, '-r', self.input, '-o', self.path])
        elif program=='prodigal':
            self.exe=__ROOTEXEDIR__+"prodigal"
            self.options="--num_threads "+p
            self.program=program
            self.sample=sample
            self.db=db
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.input=self.path+"/scaffold.fa"
            self.output=self.path+"/pred.genes"
            self.nucl=self.output+'.nucl.fa'
            self.prot=self.output+'.prot.fa'
            self.cmd=" ".join([self.exe,'-a', self.prot, '-d', self.nucl, '-f gff','-i', self.input, '-o', self.output+".gff", '-p meta', '-q'])
        elif program=="assembly_match_genes":
            self.exe=__ROOTEXEDIR__+"/bowtie2"
            self.options="--sensitive-local --no-unal -f -p "+p
            self.sample=sample
            self.program=program
            self.db=db
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.output=self.path+"/pred.genes"
            self.nucl=self.output+'.nucl.fa'
            self.prot=self.output+'.prot.fa'
            self.sam=self.output+"."+db.name+".sam"
            self.log=">>"+self.output+"."+db.name+".log 2>&1"
            self.cmd=" ".join([self.exe,"-x", db.bowtie, "-U", self.nucl, self.options,"-S", self.sam, self.log])
        elif program=="blastn":
            self.exe=__ROOTEXEDIR__+"/blastn"
            self.options="-evalue 1e-10  -outfmt 6 -max_target_seqs 1 -num_threads "+p
            self.sample=sample
            self.db=db
            self.program=program
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.output=self.path+"/pred.genes"
            self.nucl=self.output+'.nucl.fa'
            self.prot=self.output+'.prot.fa'
            self.out=self.output+"."+db.name+".matches"
            self.cmd=" ".join([self.exe,"-query", self.nucl, "-db", self.db.blast, "-out", self.out, self.options])
        elif program=="blastp":
            self.program=program
            self.exe=__ROOTEXEDIR__+"/blastp"
            self.options="-evalue 1e-10 -outfmt 6 -max_target_seqs 1 -perc_identity 60 -num_threads "+p
            self.sample=sample
            self.db=db
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.output=self.path+"/pred.genes"
            self.nucl=self.output+'.nucl.fa'
            self.prot=self.output+'.prot.fa'
            self.out=self.output+"."+db.name+".matches"
            self.cmd=" ".join([self.exe,"-query", self.prot, "-db", self.db.blast, "-out", self.out, self.options])
        elif program=="diamond_blastp":
            self.program=program
            self.exe=__ROOTEXEDIR__+"/diamond"
            self.options="--evalue 1e-10 --id 90 -k 1 -p"+p
            self.sample=sample
            self.db=db
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.output=self.path+"/pred.genes"
            self.prot=self.output+'.prot.fa'
            self.out=self.output+"."+db.name+".matches"
            self.cmd1=" ".join([self.exe,"blastp ", self.options, '-q', self.prot, "-d", self.db.diamond, "-a", self.out])
            self.cmd2=" ".join([self.exe,"view", '-a', self.out+".daa", '-o', self.out, '-f', 'tab'])
        elif program=="MetaPhlAn":
            self.program=program
            self.root=__ROOTEXEDIR__+"/metaphlan2/"
            self.exe="python "+__ROOTEXEDIR__+"/metaphlan2/metaphlan2.py "
            self.path=sample.assemblyDir+"/idba_ud/"+sample.id+"/"
            self.output=self.path+"/pred.genes"
            self.nucl=self.output+'.nucl.fa'
            self.prot=self.output+'.prot.fa'
            self.out=self.output+"."+db.name+".matches"
            self.cmd=" ".join([self.exe, self.nucl,"--input_type fasta --mpa_pkl", self.root+"db_v20/mpa_v20_m200.pkl", "--bowtie2db", self.root+"db_v20/mpa_v20_m200","-t rel_ab_w_read_stats", "--sample_id_key",sample.id, "-o", self.out, ' --biom', self.out+".biom", "--bowtie2_exe", __ROOTEXEDIR__+"/bowtie2"])
        elif program=="MetaPhlAnR":
            self.program=program
            self.root=__ROOTEXEDIR__+"/metaphlan2/"
            self.exe="python "+__ROOTEXEDIR__+"/metaphlan2/metaphlan2.py "
            self.path=sample.matchesDir
            self.output=self.path+"/alignment"
            self.out=self.output+"."+db.name+".matches"
            self.cmd=" ".join([self.exe, sample.reads1+","+sample.reads2," --bowtie2out ", self.out+".sam" ,"--input_type fastq --mpa_pkl", self.root+"db_v20/mpa_v20_m200.pkl", "--bowtie2db", self.root+"db_v20/mpa_v20_m200","-t rel_ab_w_read_stats", "--sample_id_key",sample.id, "-o", self.out, ' --biom', self.out+".biom", "--bowtie2_exe", __ROOTEXEDIR__+"/bowtie2"])
    def run(self):
        if self.program=="diamond_blastp":
            #print self.cmd1
            status=os.system(self.cmd1+">>"+log+" 2>&1")
            status=os.system(self.cmd2+">>"+log+" 2>&1")
            return status
        else:
            #print self.cmd
            status=os.system(self.cmd+">>"+log+" 2>&1")
        return status



class dataset:
    def __init__(self,dataset):
        self.dir=__ROOTDBS__+dataset+"/"
        self.name=dataset
        self.id=dataset
        self.dataset=self.dir+"dataset.fa"
        self.funcdb=load_taxodb(self.dir+"func.db")
        self.bowtie=self.dir+"dataset"
        self.blast=self.dir+"nr"
        self.diamond=self.dir+"dataset.diamond"
        self.len=load_features(self.dir+"dataset.len")
        self.func=load_features(self.dir+"dataset.func")
        self.taxo=load_features(self.dir+"dataset.taxo")
        self.taxodb=load_taxodb(self.dir+"taxo.db")

class samples:
    def __init__(self,x,path="/"):
        self.id=x[0]
        self.pid=x[1]
        self.name=x[2]
        self.set=x[3]
        self.environment=x[4]
        self.library=x[5]
        self.reads1=path+"/READS/"+x[6]
        self.reads2=path+"/READS/"+x[7]
        self.ureads=path+"/matches/"+x[0]+"/flash.extendedFrags.fastq"
        self.tree=path+"/matches/"+x[0]+"/tree.json"
        self.atree=path+"/assembly/"+x[0]+"/tree.json"
        self.path=path
        self.assemblyDir=path+"/assembly/"
        self.matchesDir=path+"/matches/"+x[0]+"/"


class SampleResults:
	def __init__(self,sample,G,pipeline,dbname,analysis, filename):
		self.sample=sample
		self.G=G
		self.pipeline=pipeline
		self.file=filename+"."+analysis+".abundance."+"results.sqlite3.db"
	def TaxonomyReadsMatches(self):
		conn=sql.connect(self.file)
		c=conn.cursor()
		table=[]
		for ni in self.G.nodes():
			level=self.G.node[ni]['level']
			rpkm=self.G.node[ni]['rpkm']
			sites=self.G.node[ni]['sites']
			matches=self.G.node[ni]['matches']
			table.append((level, ni, sites, matches, rpkm))
		c.executemany('INSERT INTO taxonomy_counts VALUES (?,?,?,?,?)', table)
		conn.commit()
		conn.close()
	def createdb(self):
		os.system("rm "+self.file+">>"+log+" 2>&1")
		conn=sql.connect(self.file)
		c=conn.cursor()
		c.execute('''CREATE TABLE taxonomy_counts (level varchar[20], name varchar[100], sites real, matches real, rpkm real)''')
		conn.commit()
	def start(self):
		self.createdb()
		self.TaxonomyReadsMatches()
	def sfunc(self):
		self.createdb()
		self.FunctionReadsMatches() #normalized data
	def createFuncDb(self,data):
		os.system("rm "+self.file+">>"+log+" 2>&1")
		conn=sql.connect(self.file)
		c=conn.cursor()
		c.execute('''CREATE TABLE function_counts (fid varchar[20], uniqueGenes real, allGenes real, relAbundance real, totalGenesRef real, Function real)''')
		c.executemany('''INSERT INTO function_counts VALUES (?,?,?,?,?,?)''', data['rpkm'])
		conn.commit()
		c.execute('''CREATE TABLE function_counts_16s (fid varchar[20], uniqueGenes real, allGenes real, relAbundance real, totalGenesRef real, Function real)''')
		c.executemany('''INSERT INTO function_counts_16s VALUES (?,?,?,?,?,?)''', data['16s'])
		conn.commit()
		conn.close()













def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d





class ViewSampleResults:
	def __init__(self,sample,pipeline,dbname,analysis,dbf):
		self.sample=sample;
		self.pipeline=pipeline
		self.analysis=analysis
		self.dbname=dbname
		self.file=dbf.sql
		self.tree=dbf.pk
	def level(self, level, type="rpkm"):
		file=self.file
		conn=sql.connect(file)
		c=conn.cursor()
		value=c.execute('SELECT name,'+type+' from taxonomy_counts where level="'+level+'"').fetchall()
		conn.close();
		return value
	def name(self, level, name):
		file=self.file
		conn=sql.connect(file)
		c=conn.cursor()
		value = c.execute('SELECT name,rpkm from taxonomy_counts where level="'+level+'" and name="'+name+'"').fetchall()
		conn.close()
		return value
	def range(self,val):
		file=self.file
		conn=sql.connect(file)
		c=conn.cursor()
		value = c.execute('SELECT min('+val+'),avg('+val+'),max('+val+') from taxonomy_counts').fetchall()
		conn.close()
		return value
	def childs_of(self,nodeID,value):
		G=nx.read_gpickle(self.tree)
		data=[]
		for i in G.successors(nodeID):
			data.append([i,G.node[i][value]])
		return data
	def all(self):
		file=self.file
		#print file
		conn=sql.connect(file)
		c=conn.cursor()
		value = c.execute('SELECT "'+self.sample.name+'", level, name, sites, matches, rpkm  from taxonomy_counts').fetchall()
		conn.close()
		return value
	def all_func(self):
		file=self.file
		#print file
		conn=sql.connect(file)
		c=conn.cursor()  #select
		value = c.execute('SELECT "'+self.sample.name+'", a.Function, a.relAbundance, a.allGenes, b.relAbundance from function_counts a inner join function_counts_16s b where a.fid==b.fid').fetchall()
		conn.close()
		return value
	def func_one_sample(self):
		file=self.file
		#print file
		conn=sql.connect(file)
		c=conn.cursor()
		value = c.execute('SELECT  Function, allGenes  from function_counts').fetchall()
		conn.close()
		return value
	def func_structure(self,pid,pip,sid):
		conn=sql.connect(self.file)
		conn.row_factory = dict_factory
		c=conn.cursor()  #select
		value = c.execute('SELECT * from ( select "'+self.sample.name+'" sample , a.Function category, a.relAbundance rpkm, a.allGenes counts, '+
						  'b.relAbundance as n16s, a.uniqueGenes as gene_counts from function_counts a inner join function_counts_16s b where a.fid==b.fid ) c ').fetchall()
		value={i['category']:i for i in value}
		try:
			dbann=json.load(open(__ROOTDBS__+self.dbname+"/dataset.description.json"))
			dbann2={}
			missing_cat=[]
			for i in value:
				try:
					dbann2[i]=dbann[i]
				except:
					dbann2[i]={'X0':i, 'X1':i, 'X2':i}
					missing_cat.append(i)
			dbann=dbann2
			#dbann={ i:dbann[i] for i in value}
		except:
			dbann=['no data']

		dbfun={i.split()[0]:i.split()[2] for i in open(__ROOTDBS__+self.dbname+"/func.db")}
		if pip=='assembly':
			dbcnt=__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/pred.genes."+self.dbname+".matches.function.genes.abundance"
		else:
			dbcnt=__ROOTPRO__+"/"+pid+"/matches/"+sid+"/alignment."+self.dbname+".matches.function.genes.abundance"

		sample_n16s={i.split()[0]:i.split()[0:4] for i in open(dbcnt+".16s")}
		sample_rpkm={i.split()[0]:i.split()[0:4] for i in open(dbcnt+".rpkm")}

		conn.close()

		return {'A':value, 'B':dbann, 'Cn16S':sample_n16s, 'CRPKM':sample_rpkm, 'D':dbfun, 'missing':missing_cat}






class result_files:
    def __init__(self,pid, aid, pip, sid, rid):
        if pip=='assembly':
            self.path=__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/"
            self.json=self.path+"pred.genes."+rid+".matches."+aid+".abundance.json"
            self.pk=self.path+"pred.genes."+rid+".matches."+aid+".abundance.pk"
            self.abundance=self.path+"pred.genes."+rid+".matches."+aid+".abundance"
            self.sql=self.path+"pred.genes."+rid+".matches."+aid+".abundance.results.sqlite3.db"
            self.silva=self.path+"pred.genes.isuezrouja.matches.taxonomy.abundance"
            self.GGenes=self.path+"pred.genes.Gbfbquhild.matches.taxonomy.abundance"
        if pip=='matches':
            self.path=__ROOTPRO__+"/"+pid+"/matches/"+sid+"/"
            self.json=self.path+"alignment."+rid+".matches."+aid+".abundance.json"
            self.pk=self.path+"alignment."+rid+".matches."+aid+".abundance.pk"
            self.abundance=self.path+"alignment."+rid+".matches."+aid+".abundance"
            self.sql=self.path+"alignment."+rid+".matches."+aid+".abundance.results.sqlite3.db"
            self.silva=self.path+"alignment.isuezrouja.matches.taxonomy.abundance"
            self.GGenes=self.path+"alignment.Gbfbquhild.matches.taxonomy.abundance"































#
