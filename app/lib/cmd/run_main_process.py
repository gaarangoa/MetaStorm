


from app.lib.main_func import mRunMetaGen
from app.lib.common import rootvar
import sys
import json
import base64

sys.path.insert(0, "/home/raid/www/cmetann/main/")

def main_run(data,refs,sid,uid,pip,dbfile, S, T):
	DBS={}
	for i in refs:
		DBS[i]=rootvar.dataset(i)
	if pip=='matches':
		st=mRunMetaGen.run(data,dbfile,DBS)
		msg='Dear CMetAnn user, <br><br> The analysis  of the sample <b>'+T[0]['sample_name']+'</b> using the un-assembled (raw) reads pipeline is done. <br> Please visit <a href="http://128.173.54.189/cmetann/login"><b>CMetAnn</b></a> to check your results <br><br><br> Than you <br><b>CMetAnn</b> Team'
		x=email.send_email(S[0]['user_name'],S[0]['user_affiliation'],'Processing sample: '+T[0]['sample_name']+" ("+sid+")", msg)
		#return 'done'
	else:
		st=mRunMetaGen.run(data,dbfile,DBS)
		msg='Dear CMetAnn user, <br><br> The analysis of the sample <b>'+T[0]['sample_name']+'</b> using the assembled reads pipeline is done. <br> Please visit <a href="http://128.173.54.189/cmetann/login"><b>CMetAnn</b></a> to check your results <br><br><br> Than you <br><b>CMetAnn</b> Team'
		x=email.send_email(S[0]['user_name'],S[0]['user_affiliation'],'Processing sample: '+T[0]['sample_name']+" ("+sid+")", msg)
		#return 'done'





inp=json.loads(base64.b64decode(sys.argv[1]))
data=inp[0]
refs=inp[1]
sid=inp[2]
uid=inp[3]
pip=inp[4]
dbfile=inp[5]
S=inp[6]
T=inp[7]

main_run(data,refs,sid,uid,pip,dbfile, S, T)

