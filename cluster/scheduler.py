import sys
sys.path.insert(0, "/groups/metastorm_cscee/MetaStorm/")

import os
from app.lib.email import Email as email
from app.lib.common.rootvar import __FILEDB__, __ROOTPRO__

import json
import base64
import paramiko
from scp import SCPClient
import re
from os import listdir
from os.path import isfile, join
import options

inpt = json.loads(base64.b64decode(sys.argv[1]))


def main(inpt):
    for run in inpt:
        inp = json.loads(base64.b64decode(run[4]))
        data = inp[0]
        refs = inp[1]
        sid = inp[2]
        uid = inp[3]
        pip = inp[4]
        dbfile = __FILEDB__  # "~/MetaStorm/SQL/projects.db"#inp[5]
        USER = inp[6]
        SAMPLE = inp[7]
        #
        # 1st send the data
        #
        if pip == "assembly":
            do = __ROOTPRO__+"/"+data['pid']+"/assembly/idba_ud/"+sid+"/"
            tof = '/home/raid/www/MetaStorm/main/Files/PROJECTS/' + \
                data['pid']+"/assembly/idba_ud/"+sid+"/"
            msg = "Dear MetaStorm user, <br><br> The analysis using the assembled reads pipeline is done. <br> Please visit <a href='bench.cs.vt.edu/MetaStorm/login'><b>MetaStorm</b></a> to check your results <br><br><br> Than you <br><b>MetaStorm</b> Team"
        else:
            do = __ROOTPRO__+"/"+data['pid']+"/matches/"+sid+"/"
            tof = '/home/raid/www/MetaStorm/main/Files/PROJECTS/' + \
                data['pid']+"/matches/"+sid+"/"
            msg = 'Dear MetaStorm user, <br><br> The analysis using the un-assembled reads pipeline is done. <br> Please visit <a href="bench.cs.vt.edu/MetaStorm/login"><b>MetaStorm</b></a> to check your results <br><br><br> Than you <br><b>MetaStorm</b> Team'
        #
        #
        print(do, tof)
        f2s = []
        for ref in refs:
            f2s.append([f for f in listdir(do) if ref in f])
        #
        #
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.load_system_host_keys()
        s.connect(options.host, options.port, options.user, options.password)
        scp = SCPClient(s.get_transport())
        #
        for i in f2s:
            for j in i:
                print(j)
                scp.put(do+j, tof+j)
        #
        scp.close()

        #
        s.close()
    return 'done'


main(inpt)
