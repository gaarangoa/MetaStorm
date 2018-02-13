import sys
#sys.path.append("../../../")
import app.lib.run.postProcessSam as sam
import app.lib.common.rootvar as root


def taxonomy_reads_pipeline(db,inputf,outputf,sample):
    tag=sample.name
    #**************************************************
    #************** merge paired end reads ************
    #**************************************************

    #**************************************************
    #************** Alignment using bowtie ************
    #**************************************************

    bowtie=root.program('bowtie2',sample)
    status=bowtie.run(db.bowtie,inputf,outputf,tag)
    # if the alignment cannot be made, stop the process and report, at this point the alignment has to be stopped.
    #if(status!=0): a=0
    #**************************************************
    #*************** Post-Processing ******************
    #**************************************************
    # filename: alignment file (sam format)
    # taxo: sequence, id.taxonomy from the dataset.taxo
    # lens: lengths of the sequences. dataset.lens
    # taxodb: taxonomy from the dataset taxo.db
    abundance=sam.process(outputf+"/"+tag+".sam", db.taxo, db.len, db.taxodb)


















#
