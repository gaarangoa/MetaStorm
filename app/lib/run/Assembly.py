import sys, os
import app.lib.common.rootvar as root
from app.lib.create_project import insert_new_project as sql
from app.lib.run import runbowtie2 as rb
import app.lib.run.postProcessSam as sam
import app.lib.run.TaxonomyProcess as txp
from app.lib.common.parse import parse_blast as pb
from app.lib.common.sqlite3_commands import update_status


def idbaud(projectid,sampleid,db,protocol,reads1, reads2, good_reads):
    #db=root.dataset(db)
    #1 get project path
    x=sql.SQL(root.filedb())
    xpath=x.project(projectid)[0][4]
    #print 'here------------'
    ###########################################################################
    #2 update the reads on the sql dataset, doit anyway, so if the sample is re run just take the new input, it could be modified.
    ###########################################################################
    val=x.exe('update samples set reads1="'+reads1+'" where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    val=x.exe('update samples set reads2="'+reads2+'" where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    ###########################################################################
    #3 get the sample full information - load the class samples
    ###########################################################################
    samples=x.exe('select * from samples where project_id="'+projectid+'" and sample_id="'+sampleid+'"')
    sample=samples[0]
    sample=root.samples(sample,xpath)
    root.mkdir(sample.assemblyDir)
    ###########################################################################
    # 4.1 Run fq2fa -  this is used by udba_ud program
    ###########################################################################
    idba_ud=root.program('idba_ud',sample,db)
    update_status(x,sampleid,db.id,protocol,"Preprocessing")
    fq2fa=root.program('fq2fa', sample,db)
    if not root.isdir(idba_ud.out): fq2fa.run() #make sure that there is a scaffold.fa file. If not, it computes again the fastq to fasta and the assembly

    ###########################################################################
    # 4.2 Run idba_ud -  assembly the samples
    ###########################################################################
    update_status(x,sampleid,db.id,protocol,"Assembling")
    idba_ud=root.program('idba_ud',sample,db)
    if not root.isdir(idba_ud.out):
        idba_ud.run();
        os.system(' cd ' + idba_ud.path + ' &&  rm kmer contig-* align-* graph-* local-contig-* reads.fa')

    ###########################################################################
    # 4.2 Run gene finder -  look at the genes over the scaffolds
    ###########################################################################
    prodigal=root.program("prodigal", sample,db)
    update_status(x,sampleid,db.id,protocol,"Finding Genes")
    if not root.isdir(prodigal.output+".gff"): prodigal.run()

    if db.name=="abcdefghij":
        print "MetaPlAn2"
        update_status(x,sampleid,db.id,protocol,"Processing")
        metaphlan=root.program('MetaPhlAn',sample,db)
        if not root.isdir(metaphlan.out): metaphlan.run()
        #print "Here 2"
        G=txp.metaphlan_taxonomy_tree(metaphlan.out)
        abn=root.SampleResults(sample,G,protocol, db.name, "taxonomy", metaphlan.out)
        abn.start()
        update_status(x,sampleid,db.id,protocol,"Done")

    if db.name=='MyTaxa':
        #print "MyTaxa"
        taxa=root.mytaxa(sample,db)
        update_status(x,sampleid,db.id,protocol,"Screening")
        if not root.isdir(taxa.output+".prot.mytaxa.fa"): taxa.pre()
        if not root.isdir(taxa.output+".MyTaxa.matches.daa"): taxa.align()
        if not root.isdir(taxa.output+".MyTaxa.align"): taxa.postd()
        if not root.isdir(taxa.output+".MyTaxa.input"): taxa.mpre()
        if not root.isdir(taxa.output+".MyTaxa.out"): taxa.run()
        update_status(x,sampleid,db.id,protocol,"Quantification")
        data=taxa.postM()
        G=txp.mytaxa_taxonomy_tree(data,taxa.output+".MyTaxa.matches.taxonomy.abundance")
        abn=root.SampleResults(sample,G,protocol, "MyTaxa", "taxonomy", taxa.output+".MyTaxa.matches")
        abn.start()
        update_status(x,sampleid,db.id,protocol,"Done")

    if not db.taxo=="none":
        print "taxonomy"
        ###########################################################################
        # 4.3 Run bowtie to find matches
        ###########################################################################
        update_status(x,sampleid,db.id,protocol,"Screening")
        if db.name=="ryaetguxun":
            blastn=root.program('diamond_blastp',sample,db)
        else:
            blastn=root.program('blastn',sample,db)
        blastn.run()
        #blastn.run()
        ###########################################################################
        # 4.4 taxonomy abundance
        ###########################################################################
        update_status(x,sampleid,db.id,protocol,"Quantification")
        abundance=pb(blastn.out, db.taxo, db.len, db.taxodb, "taxonomy", db.name, "none",good_reads)
        ###########################################################################
        # 4.5 processing Visualization
        ###########################################################################
        G=txp.taxonomy_tree(abundance,blastn.out, protocol, "taxonomy", db.name )
        abn=root.SampleResults(sample,G,protocol, db.name, "taxonomy", blastn.out)
        abn.start()
        root.updateStatus(x,projectid,sampleid,"done")
        update_status(x,sampleid,db.id,protocol,"Done")
    if not db.func=="none":
        print "functional annotation"
        update_status(x,sampleid,db.id,protocol,"Screening")
        fileso=root.result_files(projectid, "function", protocol, sampleid, db.name)
        ###########################################################################
        # 4.3 Run bowtie to find matches
        ###########################################################################
        root.updateStatus(x,projectid,sampleid,"functional annotation")
        blastn=root.program('diamond_blastp',sample,db)
        blastn.run()
        ###########################################################################
        # 4.4 taxonomy abundance
        ###########################################################################
        update_status(x,sampleid,db.id,protocol,"Quantification")
        abundance=pb(blastn.out, db.func, db.len, db.funcdb, "function", db.name, fileso.GGenes+".rpkm", good_reads)
        ###########################################################################
        # 4.5 processing Visualization
        ###########################################################################
        abn=root.SampleResults(sample,'none',protocol, db.name, "function", blastn.out)
        abn.createFuncDb(abundance)
        update_status(x,sampleid,db.id,protocol,"Done")


#print sys.argv[1]
#process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])











# here
