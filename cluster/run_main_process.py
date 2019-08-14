#!/usr/bin/python
import logging
import time
import base64
import json
from app.lib.common import rootvar
from app.lib.main_func import mRunMetaGen
import os
import sys
rootdir = '/groups/metastorm_cscee/MetaStorm/'
sys.path.insert(0, rootdir)


def my_logger(logfile=''):
    main_logfile = logfile
    logging.basicConfig(
        filename=main_logfile,
        level=logging.DEBUG,
        filemode="w",
        format="%(levelname)s %(asctime)s - %(message)s"
    )

    return logging.getLogger()


def status(pid, sid, pip, ups):
    if pip == 'matches':
        do = rootvar.__ROOTPRO__+"/"+pid+"/matches/"+sid
    else:
        do = rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid
    statusf = open(do+"/arc_run.qsub.status", 'w')
    statusf.write(ups)
    statusf.close()


def main_run(data, refs, sid, uid, pip, dbfile, U, S):
    # update status queue
    status(S['project_id'], sid, pip, 'running')
    DBS = {}
    refs = [i for i in refs if not i == "Gbfbquhild"]
    refs = ["Gbfbquhild"]+refs
    for i in refs:
        DBS[i] = rootvar.dataset(i)

    sample = [S['sample_id'], S['project_id'], S['sample_name'], S['sample_set'],
              S['environment'], S['library_preparation'], data['read1'], data['read2']]
    try:
        assert(mRunMetaGen.run(data, dbfile, DBS, USER, sample))
    except:
        pass


inp = json.loads(base64.b64decode(sys.argv[1]))
data = inp[0]
refs = inp[1]
sid = inp[2]
uid = inp[3]
pip = inp[4]
dbfile = rootvar.__FILEDB__  # "~/MetaStorm/SQL/projects.db"#inp[5]
USER = inp[6]
SAMPLE = inp[7]
pid = SAMPLE[0]['project_id']

log = my_logger(logfile=rootvar.__ROOTPRO__+"/"+pid +
                "/matches/"+sid+"/arc_run.qsub.log")

try:
    main_run(data, refs, sid, uid, pip, dbfile, USER[0], SAMPLE[0])
    # make a request to the listener in the localhost
    # get status file and check if was succesfully annotated

    if pip == 'matches':
        status = [i.split()[4] for i in open(rootdir + '/Files/PROJECTS/' + SAMPLE[0]
                                             ['project_id'] + '/' + pip + '/' + sid + '/arc_run.qsub.log') if "ERROR" in i]
        os.system('rm ' + rootdir + '/Files/PROJECTS/' +
                  SAMPLE[0]['project_id'] + '/' + pip + '/' + sid + '/*.matches')
        os.system('rm ' + rootdir + '/Files/PROJECTS/' +
                  SAMPLE[0]['project_id'] + '/' + pip + '/' + sid + '/*.daa')
    else:
        status = [i.split()[4] for i in open(rootdir + '/Files/PROJECTS/' + SAMPLE[0]
                                             ['project_id'] + '/' + pip + '/idba_ud/' + sid + '/arc_run.qsub.log') if 'ERROR' in i]
        # os.system('rm ' + rootdir + '/Files/PROJECTS/' +
        #           SAMPLE[0]['project_id'] + '/' + pip + '/idba_ud/' + sid + '/*.matches')
        os.system('rm ' + rootdir + '/Files/PROJECTS/' +
                  SAMPLE[0]['project_id'] + '/' + pip + '/idba_ud/' + sid + '/*.daa')

    message = base64.b64encode(json.dumps(status))

    external_update = 'ssh newriver1.arc.vt.edu python ' + \
        rootdir + '/listener.py ' + sys.argv[1] + ' done ' + message
    log.info("sending update to server: {}".format(external_update))

    os.system(external_update)

except Exception as inst:
    external_update = 'ssh newriver1.arc.vt.edu python ' + \
        rootdir + '/listener.py ' + sys.argv[1] + ' failed ' + message
    log.info("sending update to server: {}".format(external_update))

    os.system(external_update)
