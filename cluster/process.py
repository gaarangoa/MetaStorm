
import sys
sys.path.insert(0, "/groups/metastorm_cscee/MetaStorm/")

import os
from app.lib.email import Email as email
from app.lib.common import rootvar
import json
import base64


def qsub(ni, fi, idr, pip):

    pmem = ''
    q='normal_q'

    if pip=='assembly':
        pmem = ',pmem=100gb' 
        q = 'normal_q'       


    cmd = [
        '#!/bin/bash',
        '#PBS -l nodes=1:ppn='+rootvar.p+pmem,
        '#PBS -l walltime=144:00:00',
        '#PBS -q {}'.format(q),
        '#PBS -A computeomics',
        '#PBS -W group_list=newriver',
        '# Uncomment and add your email address to get an email when your job starts, completes, or aborts',
        '##PBS -M cmetagen@gmail.com',
        '##PBS -m bea',
        '# Change to the directory from which the job was submitted',
        '#cd ' + idr,
        # 'source /groups/metastorm_cscee/deeparg/environments/deeparg/bin/activate',
        'module load jdk/1.8.0 gcc/4.7.2 atlas',
        'python /groups/metastorm_cscee/MetaStorm/run_main_process.py ' + ni,
        'echo "the job is done"',
        # 'python /groups/metastorm_cscee/MetaStorm/scheduler.py ' + ni,
        'exit;'
    ]
    fi.write("\n".join(cmd))
    fi.close()


inp = json.loads(base64.b64decode(sys.argv[1]))
data = inp[0]
refs = inp[1]
sid = inp[2]
uid = inp[3]
pip = inp[4]
dbfile = rootvar.__FILEDB__  # "~/MetaStorm/SQL/projects.db"#inp[5]
USER = inp[6]
SAMPLE = inp[7]


# create the files for the new project/samples

try:
    os.system("mkdir -p "+rootvar.__ROOTPRO__+"/" +
              data['pid']+"/assembly/idba_ud/"+sid)
    os.system("mkdir -p "+rootvar.__ROOTPRO__ +
              "/"+data['pid']+"/assembly/RESULTS/")
    os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/matches/"+sid)
    os.system("mkdir -p "+rootvar.__ROOTPRO__ +
              "/"+data['pid']+"/matches/RESULTS/")
    os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/READS")
except:
    pass


if pip == "assembly":
    do = rootvar.__ROOTPRO__+"/"+data['pid']+"/assembly/idba_ud/"+sid+"/"
else:
    do = rootvar.__ROOTPRO__+"/"+data['pid']+"/matches/"+sid+"/"

qsub(sys.argv[1], open(do+"arc_run.qsub", 'w'), do, pip)

statusf = open(do+"arc_run.qsub.status", 'w')
statusf.write("queue")
statusf.close()

try:
    os.system('cd '+do+' && rm *.qsub.e* *.qsub.o* arc_run.log')
except:
    pass

os.system('cd '+do+' && /opt/torque/torque/bin/qsub arc_run.qsub ')

