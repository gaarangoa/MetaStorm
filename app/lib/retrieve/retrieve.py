from app.lib.common import rootvar
from app.lib.common.sqlite3_commands import update_jobs, update_status
from app.lib.create_project import insert_new_project as sql
import time
import os
import base64
import json
from app.lib.common.arc_connect import bench2archu, arcon
from app.lib.email import Email as email
import datetime
database = sql.SQL(rootvar.__FILEDB__)
import re
import logging


def get_results(job='', status=''):

    main_logfile = rootvar.__root_dir__+"/"+"/logs/retrieve.log"
    logging.basicConfig(
        filename=main_logfile,
        level=logging.INFO,
        format="%(levelname)s %(asctime)s - %(message)s"
    )

    log = logging.getLogger()

    try:
        inp = json.loads(base64.b64decode(job))
        data = inp[0]
        refs = inp[1]
        sid = inp[2]
        uid = inp[3]
        pip = inp[4]
        USER = inp[6]
        SAMPLE = inp[7]

        log = logging.getLogger()

        if pip == "assembly":
            tof = rootvar.__ROOTPRO__+"/" + \
                data['pid']+"/assembly/idba_ud/"+sid+"/"
            fromf = '/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/' + \
                data['pid']+"/assembly/idba_ud/"+sid+"/"
            msg = "Dear MetaStorm user, <br><br> The analysis using the assembled reads pipeline is done. <br> Please visit <a href='bench.cs.vt.edu/MetaStorm/login'><b>MetaStorm</b></a> to check your results <br><br><br> Thank you <br><b>MetaStorm</b> Team"
        else:
            tof = rootvar.__ROOTPRO__+"/"+data['pid']+"/matches/"+sid+"/"
            fromf = '/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/' + \
                data['pid']+"/matches/"+sid+"/"
            msg = 'Dear MetaStorm user, <br><br> The analysis using the un-assembled reads pipeline is done. <br> Please visit <a href="bench.cs.vt.edu/MetaStorm/login"><b>MetaStorm</b></a> to check your results <br><br><br> Thank you <br><b>MetaStorm</b> Team'

        # 1. Check if the job is done:

        log.info({
            "Pipeline": pip,
            "sampleID": sid,
            "ProjectID":
            data['pid'],
            "UserID": uid,
            "Status": status,
            "from": fromf,
            "tof": tof,
            "sample": SAMPLE
        })

        if status == 'done':
            # scp=arcon()
            # 2. get list of files in remote server
            try:
                SArc = os.popen(
                    'ssh gustavo1@newriver1.arc.vt.edu " ls '+fromf+'"').read().split("\n")
                reg = "matches$|daa$|txt$|scaffold.fa$|nucl.fa$|contig.fa$|prot.fa$|.qsub|^begin$|^end$|sam$"
                SArc = [i for i in SArc if not re.search(reg, i)]
            except:
                SArc = []

            log.info(('files', SArc))

            f2s = []
            for ref in refs+['nucl.fa', 'prot.fa', 'log', 'pred.genes.gff']:
                f2s.append([f for f in SArc if ref in f])

            for refi in f2s:
                for fi in refi:
                    log.debug(('Reference: ', fi))
                    os.system('scp gustavo1@newriver1.arc.vt.edu:/' +
                              fromf+fi+" "+tof+fi)

            qci = '/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/' + \
                data['pid']+"/READS/"+sid+"trim.log"
            qct = rootvar.__ROOTPRO__+"/" + \
                data['pid']+"/READS/"+sid+"trim.log"

            log.info(('QC:', qci, qct))

            os.system('scp gustavo1@newriver1.arc.vt.edu:/'+qci+" "+qct)

            for ref in refs:
                update_status(database, sid, ref, pip, "Done")
            database.commit()

            x = email.send_email(USER[0]['user_name'], USER[0]['user_affiliation'],
                                 'Processing sample: '+SAMPLE[0]['sample_name'], msg)

        update_jobs(database,
            [uid,
            SAMPLE[0]['project_id'],
            sid,
            pip,
            job[4],
            status,
            'normal',
            job[7],
            str(time.time())
            ]
        )  # update the database

        log.info(('updating database: ', [uid, SAMPLE[0]['project_id'], sid, pip, job[4], status, 'normal', job[7], str(time.time()) ]))
        database.commit()

        if status == 'failed':
            messe = "MetaStorm team: During the execution of a job under the ARC resources, an error has been triggered: <br> Please take a look at the project under <b>" + \
                SAMPLE[0]['project_id']+"</b> and sample <b>"+SAMPLE[0]['sample_id']+"</b> under the <b>"+pip+"</b> pipeline and contact the user " + \
                USER[0]['user_affiliation'] + \
                ". <br><br>Thanks for the cooperation <br>MetaStorm Team - User Assistance"
            x = email.send_email(
                'Gustavo Arango', 'gustavo1@vt.edu', 'MetaStorm', messe.strip())
            messe2 = "Dear " + \
                USER[0]['user_name'] + \
                ",<br> During the execution of one of your samples an exception has been triggered and " + \
                " the job has been terminated. <br>Please check your submission parameters (databases, fastq files, etc.) " + \
                " and try it again. <br><br> If the error persists, please contact us at cmetangen@gmail.com providing the following information:  \n" + \
                "<br><br><strong>Sample ID:</strong>" + sid + \
                "<br><strong> Project ID:</strong>" + data['pid'] + \
                "<br><strong>Pipeline:</strong>" + pip + \
                "<br><br> Thanks, <br> MetaStorm Team"
            x = email.send_email(
                USER[0]['user_name'],
                USER[0]['user_affiliation'],
                'Processing sample: ' +
                SAMPLE[0]['sample_name'], messe2.strip()
            )

            update_jobs(
                database,
                [uid, SAMPLE[0]['project_id'],
                 sid,
                 pip,
                 job[4],
                 'error',
                 'normal',
                 job[7],
                 job[8]]
            )

            database.commit()
    except Exception as e:
        log.error(str(e))
