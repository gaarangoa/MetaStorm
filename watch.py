#!/usr/bin/python

from app.lib.common import rootvar
from app.lib.common.sqlite3_commands import update_jobs, update_status
from app.lib.create_project import insert_new_project as sql
import time, os
import base64
import json
from app.lib.common.arc_connect import bench2archu, arcon
from app.lib.email import Email as email
import datetime
database=sql.SQL(rootvar.__FILEDB__)

while 1:
	try:
		jobs=database.exe("select * from jobs where priority='normal' and status!='done'")
		for job in jobs:
			inp=json.loads(base64.b64decode(job[4]))
			data=inp[0]
			refs=inp[1]
			sid=inp[2]
			uid=inp[3]
			pip=inp[4]
			dbfile=rootvar.__FILEDB__#"~/MetaStorm/SQL/projects.db"#inp[5]
			USER=inp[6]
			SAMPLE=inp[7]
			jid=job[-1]
			#
			# 1st send the data
			#
			if pip=="assembly":
				tof=rootvar.__ROOTPRO__+"/"+data['pid']+"/assembly/idba_ud/"+sid+"/"
				fromf='/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/'+data['pid']+"/assembly/idba_ud/"+sid+"/"
				msg="Dear MetaStorm user, <br><br> The analysis using the assembled reads pipeline is done. <br> Please visit <a href='bench.cs.vt.edu/MetaStorm/login'><b>MetaStorm</b></a> to check your results <br><br><br> Thank you <br><b>MetaStorm</b> Team"
			else:
				tof=rootvar.__ROOTPRO__+"/"+data['pid']+"/matches/"+sid+"/"
				fromf='/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/'+data['pid']+"/matches/"+sid+"/"
				msg='Dear MetaStorm user, <br><br> The analysis using the un-assembled reads pipeline is done. <br> Please visit <a href="bench.cs.vt.edu/MetaStorm/login"><b>MetaStorm</b></a> to check your results <br><br><br> Thank you <br><b>MetaStorm</b> Team'
			# 1. Check if the job is done:
			status=os.popen('ssh gustavo1@newriver1.arc.vt.edu "cat '+fromf+'/arc_run.qsub.status "').read().split("\n")[0]
			print json.dumps({"Pipeline":pip, "sampleID":sid,"ProjectID":data['pid'],"UserID":uid,"Status":status, "from":fromf, "tof":tof}, indent=4)
			
			 
			if status=='done':
				# scp=arcon()
				# 2. get list of files in remote server	
				SArc=os.popen('ssh gustavo1@newriver1.arc.vt.edu "ls '+fromf +
								 " | awk '{if($_!~/matches$|daa$|txt$|scaffold.fa$|nucl.fa$|contig.fa$|prot.fa$|.qsub|^begin$|^end$|sam$/){print}}'"+' "').read().split("\n")
				
				# print SArc

				for ref in refs:
					update_status(database,sid,ref,pip,"Done")
				database.commit()
				
				f2s=[]
				for ref in refs+['nucl.fa', 'prot.fa', 'log']:
					f2s.append([f for f in SArc if ref in f])
	
				for refi in f2s:
					for fi in refi:
						print fi
						os.system('scp gustavo1@newriver1.arc.vt.edu:/'+fromf+fi+" "+tof+fi)
						# scp.get(fromf+fi, tof+fi)
				
				qci='/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/'+data['pid']+"/READS/"+sid+"trim.log"
				qct=rootvar.__ROOTPRO__+"/"+data['pid']+"/READS/"+sid+"trim.log"
				
				print qci,qct
				os.system('scp gustavo1@newriver1.arc.vt.edu:/'+qci+" "+qct)
				# scp.get(qci,qct)
				
				x=email.send_email(USER[0]['user_name'],USER[0]['user_affiliation'],
							   'Processing sample: '+SAMPLE[0]['sample_name'], msg)
			
			if  status!=job[5] and not "Error:" in status: #"the status is not the same"
				update_jobs(database,[uid,SAMPLE[0]['project_id'],sid,pip,job[4],status['out'],'normal',job[7],job[8]]) #update the database
				database.commit()
			
			if "Error:" in status and job[5]!="error":
				messe="MetaStorm team: During the execution of a job under the ARC resources, an error has been triggered: <br> Please take a look at the project under <b>"+SAMPLE[0]['project_id']+"</b> and sample <b>"+SAMPLE[0]['sample_id']+"</b> under the <b>"+pip+"</b> pipeline and contact the user "+USER[0]['user_affiliation']+". <br><br>Thanks for the cooperation <br>MetaStorm Team - User Assistance"
				x=email.send_email('Gustavo Arango','gustavo1@vt.edu','MetaStorm', messe.strip())
				messe2= "Dear "+USER[0]['user_name']+",<br> During the execution of one of your samples an exception has been triggered and the job has been terminated. <br> A notification of the error has been sent to the Administrators of MetaStorm. Please check your submission parameters (databases, fastq files, etc.) and try it again. If the error persists, the MetaStorm team will contact you for further assistance. If you need inmediate assistance contact us at cmetangen@gmail.com. <br><br>This notification tool has been enabled in order to improve the efficience of MetaStorm. <br><br> Thanks, <br> MetaStorm Team"
				x=email.send_email(USER[0]['user_name'],USER[0]['user_affiliation'],'Processing sample: '+SAMPLE[0]['sample_name'], messe2.strip())
				update_jobs(database,[uid,SAMPLE[0]['project_id'],sid,pip,job[4],'error','normal',job[7],job[8]])
				database.commit()
			
			time.sleep(5)
		time.sleep(5)
	except Exception as inst:
		print "ERROR: "+str(datetime.datetime.now())+" | "+str(inst)
		x=email.send_email('Gustavo Arango','gustavo1@vt.edu', 'MetaStorm Notification: '+sid, 'error in watch.py: '+str(inst))
		time.sleep(10)
		
	
	


