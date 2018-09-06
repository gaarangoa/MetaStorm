#!/usr/bin/python
import sys
rootdir = '/groups/metastorm_cscee/MetaStorm/'
sys.path.insert(0, rootdir)

from app.lib.main_func import mRunMetaGen
from app.lib.common import rootvar

import json
import base64
import time


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
        if pip == 'matches':
            st = mRunMetaGen.run(data, dbfile, DBS, USER, sample)
        else:
            st = mRunMetaGen.run(data, dbfile, DBS, USER, sample)
            # update status done
        status(S['project_id'], sid, pip, 'done')
    except Exception as excp:
        status(S['project_id'], sid, pip,
               'Error: check your submission and try it again')
        print("this is the exception:", str(excp))


inp = json.loads(base64.b64decode(sys.argv[1]))
data = inp[0]
refs = inp[1]
sid = inp[2]
uid = inp[3]
pip = inp[4]
dbfile = rootvar.__FILEDB__  # "~/MetaStorm/SQL/projects.db"#inp[5]
USER = inp[6]
SAMPLE = inp[7]

#print USER, SAMPLE

try:
    main_run(data, refs, sid, uid, pip, dbfile, USER[0], SAMPLE[0])
    # make a request to the listener in the localhost
        os.system('ssh newriver1.arc.vt.edu python ' +
                  rootdir+'/listener.py'+sys.argv[1]+' completed')
except Exception as inst:
    os.system('ssh newriver1.arc.vt.edu python ' +
              rootdir+'/listener.py'+sys.argv[1]+' failed')
