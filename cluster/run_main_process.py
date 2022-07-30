#!/usr/bin/python
import time
import base64
import json
from app.lib.common import rootvar
from app.lib.main_func import mRunMetaGen
import os
import sys
import traceback

rootdir = '/groups/metastorm_cscee/MetaStorm/'
CLUSTER = 'dragonstooth1'

sys.path.insert(0, rootdir)


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

    sample = [S['sample_id'], S['project_id'], S['sample_name'], S['sample_set'], S['environment'], S['library_preparation'], data['read1'], data['read2']]
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

status_= []

try:
    main_run(data, refs, sid, uid, pip, dbfile, USER[0], SAMPLE[0])

    # make a request to the listener in the localhost
    # get status file and check if was succesfully annotated

    if pip == 'matches':
        status_ = [ i.strip().split(' - ')[-1] for i in open(rootdir + '/Files/PROJECTS/' + SAMPLE[0]['project_id'] + '/' + pip + '/' + sid + '/arc_run.qsub.log') if "E$
        os.system('rm ' + rootdir + '/Files/PROJECTS/' + SAMPLE[0]['project_id'] + '/' + pip + '/' + sid + '/*.matches')
        os.system('rm ' + rootdir + '/Files/PROJECTS/' + SAMPLE[0]['project_id'] + '/' + pip + '/' + sid + '/*.daa')
    else:
        status_ = [i.strip().split(' - ')[-1] for i in open(rootdir + '/Files/PROJECTS/' + SAMPLE[0]['project_id'] + '/' + pip + '/idba_ud/' + sid + '/arc_run.qsub.log'$
        os.system('rm ' + rootdir + '/Files/PROJECTS/' + SAMPLE[0]['project_id'] + '/' + pip + '/idba_ud/' + sid + '/*.daa')

    message = base64.b64encode(json.dumps(status_))
    os.system('ssh {}.arc.vt.edu python '.format(CLUSTER) + rootdir + '/listener.py ' + sys.argv[1] + ' done ' + message)

except Exception as inst:
    print('Error',traceback.format_exc())
    os.system('ssh {}.arc.vt.edu python '.format(CLUSTER) + rootdir + '/listener.py '+sys.argv[1]+' failed ' + 'failed')