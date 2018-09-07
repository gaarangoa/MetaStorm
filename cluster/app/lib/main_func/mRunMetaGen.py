from app.lib.run.MAIN_PROCESS import process as MP
from app.lib.run.Assembly import idbaud as idba
import os,re
from app.lib.common import module
from app.lib.common import rootvar
import json
from app.lib.preprocessing import functions as pre
import logging
import traceback
import base64

def run(data,main_db,DBS, uinfo, sample):
    project_id=str(data['pid'])
    pipeline=str(data['pip'])
    reads1=str(data['read1'])
    reads2=str(data['read2'])
    sample_id=str(data['sid'])
    user_id=str(data['uid'])
    refs = data["rids"]
    refs = [i for i in refs if not i == "Gbfbquhild"]
    refs = ["Gbfbquhild"] + refs

    if pipeline == "matches":
        logfile=rootvar.__ROOTPRO__ + "/" + project_id + "/matches/" + sample_id + "/arc_run.qsub.log"
    else:
        logfile=rootvar.__ROOTPRO__ + "/" + project_id + "/assembly/idba_ud/" + sample_id + "/arc_run.qsub.log"

    logging.basicConfig(
        filename=logfile,
        level=logging.ERROR,
        filemode="w",
        format="%(levelname)s %(asctime)s - %(message)s"
    )

    log = logging.getLogger()

    try:
        assert(refs[0])
    except:
        e = traceback.format_exc()
        log.error(base64.b64encode(json.dumps(
            {
                "status": "failed",
                "exception": str(e),
                "sample_id": sample_id,
                "reference_id": 'unknown'
            }
        )))
        return False

    rdir=rootvar.__ROOTPRO__+"/"+project_id+"/READS/"
    log.info('running trimmomatic')
    trim=pre.trimmomatic(rdir+reads1,rdir+reads2,rdir,sample_id)
    trim.run()
    reads1=reads1.replace(".gz","")
    reads2=reads2.replace(".gz","")
    #print pipeline
    ##################################################################################################
    ##### This is very important,
    ##### First: Check if the GREENGENES database has been used for finding the 16s rRNAs, if not,
    ##### The greengenes database is force d to run this database will run first for normalization purposes.
    ##################################################################################################
    if pipeline=="assembly": greengenes_file=rootvar.__ROOTPRO__+"/"+project_id+"/assembly/idba_ud/"+sample_id+"/pred.genes.Gbfbquhild.matches"
    if pipeline=="matches": greengenes_file=rootvar.__ROOTPRO__+"/"+project_id+"/matches/"+sample_id+"/pred.genes.Gbfbquhild.matches"
    #_______________________________________________________________##################################
    #
    # Get the number of reads
    log.info('running pipeline %s'%(pipeline,))
    tfile = trim.outd + sample_id + 'trim.log'
    log.info('trimmomatic log file: %s'%(tfile,) )
    good_reads = 0
    for i in open(tfile):
        if "Input Read Pairs:" in i:
            i=i.split()
            good_reads=float(i[6]) # the number of high quality reads after trimming and quality filter

    if pipeline=="matches":
        for ref in refs:
            log.info('Processing %s with reference id: %s' % (sample_id, ref))
            try:
                val = MP(project_id, sample_id, DBS[ref], "matches", reads1, reads2, good_reads, sample)
            except:
                e = traceback.format_exc()
                log.error(base64.b64encode(json.dumps(
                    {
                        "status": "failed",
                        "exception": str(e),
                        "sample_id": sample_id,
                        "reference_id": ref
                    }
                )))
    #
    #this is for the aseembly section
    #
    if pipeline=="assembly":
        for ref in refs:
            try:
                idba(project_id, sample_id, DBS[ref], "assembly", reads1, reads2, good_reads, sample)
            except:
                e = traceback.format_exc()
                log.error(base64.b64encode(json.dumps(
                    {
                        "status": "failed",
                        "exception": str(e),
                        "sample_id": sample_id,
                        "reference_id": ref
                    }
                )))


    if not rootvar.isdir(rdir+reads1+".gz"):
        os.system('gzip '+rdir+reads1+' >> '+rootvar.log+" 2>&1")
        os.system('rm '+rdir+reads1+' >> '+rootvar.log+" 2>&1")
    else:
        os.system('rm '+rdir+reads1+' >> '+rootvar.log+" 2>&1")

    if not rootvar.isdir(rdir+reads2+".gz"):
        os.system('gzip '+rdir+reads2+' >> '+rootvar.log+" 2>&1")
        os.system('rm '+rdir+reads2+' >> '+rootvar.log+" 2>&1")
    else:
        os.system('rm '+rdir+reads2+' >> '+rootvar.log+" 2>&1")

    return 'success'










