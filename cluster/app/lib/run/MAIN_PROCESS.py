import sys
#import app.lib.common.rootvar as root
from app.lib.create_project import insert_new_project as sql
from app.lib.run import runbowtie2 as rb
import app.lib.run.postProcessSam as sam
import app.lib.run.TaxonomyProcess as txp
import app.lib.common.rootvar as root
from app.lib.preprocessing import functions as pre
import os
import subprocess
from app.lib.common.parse import parse_sam
from app.lib.common.parse import parse_diamond_blastx as pdx
from app.lib.common.sqlite3_commands import update_status
from app.lib.common.parse import parse_blast as pb

p=root.p

###### read matching pipeline #####

def process(projectid,sampleid,db,protocol,reads1, reads2, good_reads, sample):
    #db=root.dataset(db)
    #x=sql.SQL(root.filedb())
    #xpath=x.project(projectid)[0][4]
    #print xpath
    #val=x.exe('update samples set reads1="'+reads1+'" where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    #val=x.exe('update samples set reads2="'+reads2+'" where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    #samples=x.exe('select * from samples where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    #sample=sampleid
    #print sample
    sample=root.samples(sample)
    root.mkdir(sample.matchesDir)
    rdir=root.__ROOTPRO__+"/"+projectid+"/READS/"

    if db.name=="abcdefghij":
        #print "MetaPhlAnn"
        #update_status(x,sampleid,db.id,protocol,"Processing")
        metaphlan=root.program('MetaPhlAnR',sample,db)
        if not root.isdir(metaphlan.out): metaphlan.run()
        G=txp.metaphlan_taxonomy_tree(metaphlan.out)
        abn=root.SampleResults(sample,G,protocol, db.name, "taxonomy", metaphlan.out)
        abn.start()
        #update_status(x,sampleid,db.id,protocol,"Done")

    if not db.taxo=="none":
        # run bowtie using the paired end reads
        #update_status(x,sampleid,db.id,'matches',"Screening")
        cmd=" ".join([root.__ROOTEXEDIR__+'bowtie2', '--fast-local --no-discordant -p '+p+' --no-unal --no-hd --no-sq -x', db.bowtie, '-1', sample.reads1, '-2', sample.reads2, '-S', sample.matchesDir+'/alignment.'+db.id+'.matches >>', root.log, '2>&1'])
        if not root.isdir(sample.matchesDir+'/alignment.'+db.id+'.matches'): os.system(cmd)
        #process output in sam format to get genes and number of reads per gene.
        #update_status(x,sampleid,db.id,protocol,"Quantification")
        #if not root.isdir(sample.matchesDir+'/alignment.'+db.id+'.matches.taxonomy.abundance.results.sqlite3.db'):
        abundance=parse_sam(sample.matchesDir+'/alignment.'+db.id+'.matches', db, good_reads)
        G=txp.taxonomy_tree(abundance,sample.matchesDir+'/alignment.'+db.id+'.matches',protocol,"taxonomy",db.id)
        abn=root.SampleResults(sample,G,protocol,db.id, "taxonomy",sample.matchesDir+'/alignment.'+db.id+'.matches') # Store data in the sql TABLE
        abn.start()
        #update_status(x,sampleid,db.id,protocol,"Done")
        return 'success'
    if not db.func=="none":
        fileso=root.result_files(projectid, "function", protocol, sampleid, db.name)
        #Merge paired ends
        #update_status(x,sampleid,db.id,protocol,"Merge")
        #cmd=" ".join(['python', root.__ROOTEXEDIR__+"pairend_join.py -s -p "+p+" -m 8 -o ", sample.matchesDir+'/merged.reads.fastq', sample.reads1, sample.reads2])
        cmd=" ".join([root.__ROOTEXEDIR__+"fq2fa --merge ", sample.reads1, sample.reads2, sample.matchesDir+"/merged.reads.fasta"])
        #print cmd
        #root.flog(cmd)#print cmd
        if not root.isdir(sample.matchesDir+'/merged.reads.fasta'): os.system(cmd)
        #Get fasta files
        #cmd = ' '.join([root.__ROOTEXEDIR__+'/seqtk seq -a',sample.matchesDir+'/merged.reads.fastq >', sample.matchesDir+'/merged.reads.fasta'])
        #if not root.isdir(sample.matchesDir+'/merged.reads.fasta'):
        #    os.system(cmd)
        #BlastX from diamond
        #update_status(x,sampleid,db.id,protocol,"Screening")
        dout=sample.matchesDir+'alignment.'+db.id
        din=sample.matchesDir+'/merged.reads.fasta'
        cmd=' '.join([root.__ROOTEXEDIR__+'/diamond blastx --id 60 -p '+p+' -k 10 -e 1e-5 -d', db.diamond, '-a', dout+'.pre', '-q', din, '>>', root.log, "2>&1"])
        if not root.isdir(dout+'.daa'): os.system(cmd)
        cmd=' '.join([root.__ROOTEXEDIR__+'/diamond view -a', dout+'.pre.daa', '-o', dout+'.matches -f tab', ">>", root.log, "2>&1"])
        if not root.isdir(dout+'.matches'): os.system(cmd)
        # parse diamond output
        #update_status(x,sampleid,db.id,protocol,"Quantification")
        #if not root.isdir(sample.matchesDir+'/alignment.'+db.id+'.matches.function.abundance.results.sqlite3.db'):
        abundance=pb(dout+'.matches', db.func, db.len, db.funcdb, "function", db.name, fileso.GGenes+".rpkm", good_reads,'matches')
        #abundance=pdx(dout+'.matches', db, good_reads)
        abn=root.SampleResults(sample,'none',protocol, db.name, "function", dout+'.matches')
        abn.createFuncDb(abundance)
        #update_status(x,sampleid,db.id,protocol,"Done")
        #os.system('rm '+sample.matchesDir+'/merged.reads.fastq >> '+root.log+" 2>&1")
        os.system('rm '+sample.matchesDir+'/merged.reads.fasta >> '+root.log+" 2>&1")
        return 'success'











# here'''
