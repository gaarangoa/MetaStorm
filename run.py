import sys
sys.path.insert(0, "/home/raid/www/MetaStorm/main/")

from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for
import os,re
from app.lib.common import module
from app.lib.common import rootvar
import json
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import sqlite3
from flask import g
from flask import request
import base64
import sklearn
from app.lib.email import Email as email
import time
import requests
import threading



app = Flask(__name__)


DATABASE=rootvar.__FILEDB__
main_db=DATABASE

def connect_db():
	return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
	g.db=connect_db()

@app.teardown_request
def teardown_request(exception):
	if hasattr(g,'db'):
		g.db.close()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def insert(table, fields=(), values=()):
    # g.db is the database connection
    cur = g.db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.db.commit()
    id = cur.lastrowid
    cur.close()
    return id







#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
# SECTION: login
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************



def csession(request):
	try:
		data = request.get_json()
		uid=str(data['uid'])
		if uid=="TesREPDooc73Ohw": return True
		browser = request.headers.get('User-Agent')
		ip=request.remote_addr
		session_info=query_db('select * from session where uid="'+uid+'" and ip="'+ip+'" and browser="'+browser+'" and status="online"')[0]
		return True
	except Exception as inst:
		return False


@app.route('/login')
def login():
	return render_template('pages/examples/login.html')
	#credentials=query_db('select * from user')
	#return str(credentials)

@app.route('/register')
def register():
	return render_template('pages/examples/register.html')


@app.route('/lgn', methods=['GET','POST'])
def lgn():
	password=request.form.get("password",None)
	email=request.form.get("eMail",None)
	browser = request.headers.get('User-Agent')
	userIP=request.remote_addr
	credentials=query_db('select * from user where user_affiliation="'+str(email)+'" and user_password="'+str(password)+'"')
	#return jsonify(status=credentials)
	if not credentials:
		return jsonify(status='fatal')
	elif not credentials[0]['user_password']==password:
		return jsonify(status='fatal')
	g.db.execute("INSERT or REPLACE into session VALUES (?,?,?,?)", (credentials[0]['user_id'],userIP, browser, 'online'))
	g.db.commit()
	return jsonify(uname=credentials[0]['user_name'], uid=credentials[0]['user_id'], IP=userIP, browser=browser)


@app.route('/muser', methods=['GET','POST'])
def metadatafhtml():
	#if not csession(request): return render_template("pages/examples/login.html")
	return render_template('main_user_page.html')


@app.route('/logout', methods=['GET','POST'])
def logout():
	browser = request.headers.get('User-Agent')
	userIP=request.remote_addr
	data = request.get_json()
	uid=data['uid']
	g.db.execute("INSERT or REPLACE into session VALUES (?,?,?,?)", (uid,userIP, browser, 'offline'))
	g.db.commit()
	return render_template("pages/examples/login.html")



@app.route('/phpupload')
def phpupload():
	#return 'oki'
	return render_template("plupload/examples/jquery/jquery_ui_widget.html")


from os import listdir
from os.path import isfile, join
@app.route('/get_raw_reads_names', methods=['GET','POST'])
def get_raw_reads_names():
	try:
		data = request.get_json()
		pid = data['pid']
		mypath=rootvar.__ROOTPRO__+"/"+pid+"/READS/"
		onlyfiles = sorted([f.replace(".arc.md5","") for f in listdir(mypath) if ".gz.arc.md5" in f and not "unpaired" in f])
		return jsonify(files=onlyfiles)
	except Exception as inst:
		return jsonify(status="ERROR", error=str(inst))







#******************************************************************************
#******************************************************************************
## change password
#******************************************************************************
#******************************************************************************


@app.route('/change_password', methods=['GET','POST'])
def change_password():
	try:
		oldp1=request.form.get("oldp1",None)
		new1=request.form.get("newp1",None)
		new2=request.form.get("newp2",None)
		uid=request.form.get('pass_user_id', None)

		if new1!=new2: return 'Error: passwords do not match'

		cpass=query_db('select user_password from user where user_id="'+str(uid)+'"')
		if cpass[0]['user_password']==oldp1:
			g.db.execute('UPDATE user SET user_password="'+new1+'" WHERE user_id="'+uid+'"')
			g.db.commit()
			return 'Password has been updated!'
		else:
			return 'Error: old password does not match'

	except Exception as inst:
		return jsonify(status="ERROR", error=str(inst))





### forgot password
@app.route('/forgot_pass', methods=['GET','POST'])
def forgot_pass():
	try:
		data = request.get_json()
		gemail =  data['email']
		credentials=query_db('select * from user where user_affiliation="'+str(gemail)+'"')
		email.send_email(credentials[0]['user_name'], gemail, 'MetaStorm request', 'Dear MetaStorm user, <br> This is your password <br><br><br>' + credentials[0]['user_password']+'<br><br>MetaStorm Team')
		return jsonify(status='the password has been sent to your '+gemail+' personal email')
	except Exception as inst:
		return str(inst)





#******************************************************************************
# SECTION: Insert user
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
@app.route('/insert_new_user', methods=['GET','POST'])
def insert_new_user():
	name=request.form.get("FullName",None)
	eMail=request.form.get("eMail",None)
	organization=request.form.get("Organization",None)
	country=request.form.get("Country",None)
	IAgree=request.form.get("IAgree",None)
	id=rootvar.get_alphabet(15)
	password=rootvar.get_alphabet(20)
	date=time.strftime("%d/%m/%Y")
	try:
		g.db.execute('INSERT INTO user (user_id,user_password,user_name,user_affiliation,organization,country,date) VALUES (?,?,?,?,?,?,?)',(id,str(password),str(name),str(eMail),str(organization),str(country),date))
		g.db.commit()
		msg="Dear MetaStorm user, <br> You have been granted with access to our web service. Please login at <a href='bench.cs.vt.edu/MetaStorm/login'>MetaStorm</a> in order to use the web resource <br> User - "+eMail+"<br> Password - "+password+"<br><br><b>MetaStorm</b> team"
		subject="MetaStorm - New account requested"
		#msg="we are done"
		g.db.execute('INSERT INTO user_projects (user_id,project_id) VALUES(?,?)',(id,'pNAr1xdrsO6H7xs'))
		g.db.commit()
		email.send_email(name,eMail,subject,msg)
		return jsonify(ms=id)
	except Exception as inst:
		return jsonify(status="ERROR", error=str(inst))


#******************************************************************************
# BEGIN: GET ALL info
#******************************************************************************
@app.route('/GetAllInfo', methods=['GET','POST'])
def GetAllInfo():
	if not csession(request): return render_template("pages/examples/login.html")
	data = request.get_json()
	uid=str(data['uid'])
	try:
		userInfo=query_db('select * from user where user_id="'+uid+'"')
		projectsInfo=query_db('select e.project_id project_id, e.project_name project_name from (select c.project_id project_id, d.project_name project_name, c.user_id user_id from  (select b.project_id project_id, a.user_id user_id from user a inner join user_projects b on a.user_id=b.user_id) c inner join project d on c.project_id=d.project_id) e where e.user_id="'+uid+'"')
		samplesInfo=query_db('select * from (select e.user_id, e.project_id, e.project_name, f.sample_id, f.sample_name from  (select c.project_id project_id, d.project_name project_name, c.user_id user_id from  (select b.project_id project_id, a.user_id user_id from user a inner join user_projects b on a.user_id=b.user_id) c inner join project d on c.project_id=d.project_id) e inner join samples f on e.project_id=f.project_id) g where g.user_id="'+uid+'"')
		return jsonify(uname=userInfo[0]['user_name'], email=userInfo[0]['user_affiliation'], affiliation=userInfo[0]['organization'], projects=projectsInfo, samples=samplesInfo)
	except Exception as inst:
		return jsonify(status="ERROR", error=str(inst))








@app.route('/vsession', methods=['GET','POST'])
def vsession():
	if not csession(request):
		return "offline"
	else:
		return "online"























#******************************************************************************
# BEGIN: Submit a new project
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************

@app.route('/metadata')
def metadatahtml():
	return render_template('metadata.html')

@app.route('/insertproject', methods=['GET','POST'])
def insert_project():
	try:
		data = request.get_json()
		name = str(data['name'])
		userID=str(data['userID'])
		description = str(data['description'])
		if userID=="TesREPDooc73Ohw": return 'User not allowed'
		id=rootvar.get_alphabet(15)
		resu=g.db.execute("INSERT INTO project VALUES (?,?,?,?,?) ",(id,name,"lock",description,rootvar.__ROOTPRO__+"/"+id))
		g.db.commit()
		resu=g.db.execute("INSERT INTO user_projects VALUES (?,?)",(userID,id))
		g.db.commit()
		# remove an item: x.exe("delete from project where project_id==1")
		if not os.path.exists(rootvar.__ROOTPRO__+"/"+id): os.makedirs(rootvar.__ROOTPRO__+"/"+id)
		return jsonify(name=name, id=id, description=description)
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: Update project link
#******************************************************************************
@app.route('/UpdateProject', methods=['GET','POST'])
def UpdateProject():
    return render_template('UpdateProject.html')

@app.route('/UpdateProject_reads', methods=['GET','POST'])
def UpdateProject_reads():
    return render_template('Update_Project_Reads_2.php')

@app.route('/ExploreProject', methods=['GET','POST'])
def ExploreProject():
    return render_template('ExploreProject.html')

#******************************************************************************
# BEGIN: consult
#******************************************************************************
@app.route('/consult', methods=['GET','POST'])
def consult():
	try:
		data = request.get_json()
		consult=str(data['sql'])
		value=query_db(consult)
		g.db.commit()
		return jsonify(data=list(value), consult=consult)
	except Exception as inst:
		return "ERROR: "+str(inst)

# execute a sql command
@app.route('/sqlgo', methods=['GET','POST'])
def sqlgo():
	try:
		data = request.get_json()
		#return jsonify(data['sql'])
		exe=base64.b64decode(str(data['sql']))

		#print exe
		g.db.execute(exe);
		g.db.commit();
		return jsonify('success')
	except Exception as inst:
		return "error: "+str(inst)



#******************************************************************************
# BEGIN: Remove Project
#******************************************************************************
@app.route('/remove_element', methods=['GET','POST'])
def remove_element():
	try:
		data = request.get_json()
		uid=str(data['uid'])
		pid=str(data['pid'])
		if uid=="TesREPDooc73Ohw": return 'User not allowed'
		dir_to_sid=query_db(' select * from project where project_id="'+pid+'"')[0]['project_path']
		g.db.execute('delete from user_projects where user_id="'+uid+'" and project_id="'+pid+'"')
		g.db.execute('delete from project where project_id="'+pid+'"')
		g.db.execute('delete from samples where project_id="'+pid+'"')
		g.db.commit()
		os.system('rm -r '+dir_to_sid)
		return 'ok'
	except Exception as inst:
		return "ERROR: "+str(inst)





























#******************************************************************************
# BEGIN: Insert Samples
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
from random import randint

@app.route('/insertsamples',methods=['GET','POST'])
def insert_samples():
	try:
		data = request.get_json()
		samples=data['samples']
		pid=data['pid']
		uid=data['uid']
		pip=data['pip']
		if uid=="TesREPDooc73Ohw": return 'User not allowed'
		sdata=[]
		for sample in samples:
			if sample != []:
				id=rootvar.get_alphabet(25)
				item=(id,str(pid))
				for i in sample:
					item+=(str(i),)
				sdata.append(item)
				g.db.execute("INSERT INTO samples VALUES (?,?,?,?,?,?,?,?,?,?)",(item[:-2]+("","")+item[-2:]))
				g.db.commit()
				#x.insert("samples",item+("",""))
				g.db.execute('INSERT INTO project_status  VALUES (?,?,?,?,?)',(uid,pid,id,'created',pip))
				g.db.commit()
		samples=[]
		ids={}
		for item in sdata:
			samples.append({'id':item[0]})
			ids[item[0]]=item[2]
		##print samples
		return jsonify(samples=samples, ids=ids)
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: Remove Sample
#******************************************************************************
@app.route('/removesample',methods=['GET','POST'])
def remove_sample():
	try:
		data = request.get_json() #{'pid':'bcrxuradwctalvl', 'sid':'sid', 'pip':'pip'}#
		pid=str(data['pid'])
		sid=str(data['sid'])
		pip=str(data['pip'])
		uid=str(data['uid'])
		if uid=="TesREPDooc73Ohw": return 'User not allowed'
		g.db.execute('delete from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
		g.db.execute('delete from project_status where project_id="'+pid+'" and sample_id="'+sid+'"')
		g.db.commit()
		if pip=="assembly":
			dir_to_sid=query_db(' select * from project where project_id="'+pid+'"')[0]['project_path']+"/"+pip+"/idba_ud/"+sid+"/"
		else:
			dir_to_sid=query_db(' select * from project where project_id="'+pid+'"')[0]['project_path']+"/"+pip+"/"+sid+"/"
		os.system('rm -r '+dir_to_sid)
		return dir_to_sid
	except Exception as inst:
		return "ERROR: "+str(inst)










































#******************************************************************************
#******************************************************************************
# BEGIN: Upload Files
#******************************************************************************
#******************************************************************************

'''app.config['ALLOWED_EXTENSIONS'] = set(['fasta','function',  'fastq', 'csv','db','func','taxo','fa','fq','fun','gz'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']'''


from werkzeug import secure_filename
import requests
from multiprocessing import Process


def load_file(file,projectid):
	try:
		app.config['UPLOAD_FOLDER']=rootvar.__ROOTPRO__+"/"+projectid+"/READS/"
		if not os.path.exists(rootvar.__ROOTPRO__+"/"+projectid+"/READS/"): os.makedirs(rootvar.__ROOTPRO__+"/"+projectid+"/READS/")
		if file:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		g.db.execute("INSERT or REPLACE INTO fastqFiles VALUES (?,?,?,?)",(projectid+'_'+file.filename,projectid,file.filename,'done'))
		g.db.commit()
	except Exception as inst:
		g.db.execute("INSERT or REPLACE INTO fastqFiles VALUES (?,?,?,?)",(projectid+'_'+file.filename,projectid,file.filename, inst))
		g.db.commit()

@app.route('/uploadajax', methods=['GET','POST'])
def uploadajax():
	try:
		file = request.files['file']
		projectid=request.form.get("projectid",None)
		Process(target=load_file, args=(file,projectid)).start()
		#load_file(file,projectid)
		return file.filename
	except Exception as inst:
		return "ERROR: "+str(inst)










#******************************************************************************
# BEGIN:  reference dataset
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
# data is stored in reference, but all the other files need to be saved intot he reference_format directory.

from app.lib.create_project import insert_new_project as sql

@app.route('/upload_reference', methods=['GET','POST'])
def upload_dataset():
    pid = request.args.get('pid', "None", type=str)
    return render_template('upload_reference_dataset.html')

#******************************************************************************
# BEGIN: register dataset
#******************************************************************************
@app.route('/register_dataset', methods=['GET','POST'])
def register_dataset():
	try:
		data =  request.get_json() #{'rname':'test', 'rtype':'prot', 'rdesc':'test', 'uid':'test'}#
		rname=data["rname"]
		rtype=data["rtype"]
		rdesc=data["rdesc"]
		uid=data["uid"]
		if uid=="TesREPDooc73Ohw": return 'User not allowed'
		#x=sql.SQL(rootvar.__FILEDB__)
		rid=rootvar.get_alphabet(10)
		rpath=rootvar.__ROOTDBS__+rid
		ref_format_path=rootvar.__ROOTDBS__+rid
		rootvar.mkdir(rpath)
		g.db.execute('INSERT INTO reference VALUES (?,?,?,?,?,?,?,?,?,?,?)', (rid,rname,rtype,rdesc,rpath,uid,"none","none","none","created",ref_format_path))
		g.db.commit()
		return jsonify(rid=rid)
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: upload files
#******************************************************************************
def upload(file,dir):
	app.config['UPLOAD_FOLDER']=dir
	rootvar.mkdir(dir)
	if file:
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/uploadref', methods=['GET','POST'])
def uploadref():
	try:
		rid=request.form.get("rid",None)
		file =request.files['file']
		dir=rootvar.__ROOTDBS__+"/"+rid+"/"
		upload(file,dir)
		return(jsonify(fname=file.filename,rid=rid))
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: process dataset
#******************************************************************************
import app.lib.make_db.GetUniqueIdentifier as updb
import app.lib.make_db.get_seq_length as glen
import app.lib.make_db.make_reference_formats as formatdb
from app.lib.common.arc_connect import bench2archu, arcon
from app.lib.email import Email as email
from os import listdir
from os.path import isfile, join

@app.route('/process_up_ref_dataset', methods=['GET','POST'])
def process_up_ref_dataset():
	try:
		data = request.get_json() #{'taxofile':'none', 'functfile':'DATASET.func', 'rid':'eyzbhakkpq', 'seqfile':'dataset.fa', 'rname':'card_sample', 'uid':'ihqvnteormayzoy'}#
		#x=sql.SQL(main_db)

		g.db.execute('UPDATE reference SET seqfile="'+data['seqfile']+'",  taxofile="'+data['taxofile']+'", functfile="'+data['functfile']+'" WHERE reference_id="'+data['rid']+'"')
		g.db.commit()
		refdb=query_db('SELECT * from reference where reference_id="'+data['rid']+'"')[0]
		#return jsonify(data=refdb)
		#return jsonify(data=data)
		if str(data["taxofile"])!="none":
			updb.GetUniqueIdentifier(refdb['reference_path'],refdb['reference_format_path'],refdb['taxofile'],"taxo",g,data['rid']) # for taxonomy
			glen.seqlen(refdb['reference_path']+'/'+refdb['seqfile'],refdb['reference_format_path']+'/dataset.len')
			formatdb.main(refdb['reference_path'],refdb['reference_format_path'],refdb['sequence_type'],refdb['seqfile'], g, data['rid'])
			g.db.execute('UPDATE reference SET status="done" WHERE reference_id="'+data['rid']+'"')
		if str(data["functfile"])!="none":
			updb.GetUniqueIdentifier(refdb['reference_path'],refdb['reference_format_path'],refdb['functfile'],"func",g,data['rid']) # for function
			glen.seqlen(refdb['reference_path']+'/'+refdb['seqfile'],refdb['reference_format_path']+'/dataset.len')
			formatdb.main(refdb['reference_path'], refdb['reference_format_path'],refdb['sequence_type'], refdb['seqfile'], g, data['rid'])
			rootvar.tsv2json(refdb['reference_format_path']+'/dataset.description',"\t")
			g.db.execute('UPDATE reference SET status="done" WHERE reference_id="'+data['rid']+'"')
		g.db.commit()

		## make the directory at arc
		arcdir='/groups/metastorm_cscee/MetaStorm/Files/REFERENCE/'
		os.system('ssh gustavo1@newriver1.arc.vt.edu "mkdir -p '+arcdir+data['rid'] + '"')
		# scp=arcon()

		## move the files to arc
		# for fi in listdir(refdb['reference_path']):
		os.system('scp '+refdb['reference_path']+'/* gustavo1@newriver1.arc.vt.edu:'+arcdir+"/"+data['rid']+"/")
		os.system('rm -r'+refdb['reference_path']+"/*")

		return 'ok'
	except Exception as inst:
		return "ERROR: "+str(inst)























































#******************************************************************************
# BEGIN: Run samples
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************
from app.lib.common.arc_connect import bench2archu
from app.lib.common.sqlite3_commands import update_jobs, update_status

@app.route('/RunMetaGen', methods=['GET','POST'])
def RunMetaGen():
	try:
		data = request.get_json()
		refs=data["rids"]
		sid=data['sid']
		uid=data['uid']
		pip=data['pip']
		msg=data['msg']

		if uid=="TesREPDooc73Ohw": return 'User not allowed'
		S=query_db('select * from user  where user_id="'+uid+'"')
		T=query_db('select * from samples where sample_id="'+sid+'"')
		date=time.strftime("%m/%d/%Y")
		pid=T[0]['project_id']
		arg=base64.b64encode(json.dumps([data,refs,sid,uid,pip,rootvar.__FILEDB__, S, T]))
		SArc=bench2archu('python /groups/metastorm_cscee/MetaStorm/process.py ' + arg)

		x=sql.SQL(rootvar.__FILEDB__)
		update_jobs(x,[uid,T[0]['project_id'],sid,pip,arg,'queue','normal',date,SArc['out'].split(".")[0]])

		val=x.exe('update samples set reads1="'+data['read1']+'" where project_id="'+data['pid']+'" and sample_id="'+sid+'"')
		val=x.exe('update samples set reads2="'+data['read2']+'" where project_id="'+data['pid']+'" and sample_id="'+sid+'"')



		for ref in refs:
			update_status(x,sid,ref,pip,"queue")
			if not x.exe('select * from '+pip+' where sample_id="'+sid+'" and datasets="'+ref+'"'):
				x.c.execute('INSERT OR IGNORE INTO '+pip+' VALUES (?,?,?,?)', (sid,uid,pid,ref))
				x.commit()

		x.close()


		try:
			os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/assembly/idba_ud/"+sid)
			os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/assembly/RESULTS/")
			os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/matches/"+sid)
			os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/matches/RESULTS/")
			os.system("mkdir -p "+rootvar.__ROOTPRO__+"/"+data['pid']+"/READS")
		except:
			pass

		x=email.send_email(S[0]['user_name'],S[0]['user_affiliation'],
							   'Processing sample: '+T[0]['sample_name'], "Dear MetaStorm User, <br><br><br> the sample <b>"+
							   T[0]['sample_name']+
							   '</b> has been submitted into the MetaStorm server. It will run the <b>'+pip+'</b> pipeline <br><br>'
							   'The time for making the analysis depends on the current web traffic and availability of the web server. Once the '+
							   'analysis is done you will receive a notification via email. <br><br><br><br>'+
							   'Thank you<br><b>MetaStorm Team</b>')

		return jsonify(SArc)
	except Exception as inst:
		return "ERROR: "+str(inst)






#******************************************************************************
# BEGIN: ViewSample
#******************************************************************************
#******************************************************************************
#******************************************************************************
#******************************************************************************

@app.route('/ViewSample', methods=['GET','POST'])
def viewsample():
    pid = request.args.get('pid', "None", type=str)
    return render_template('ViewSample.html')

@app.route('/ViewSampleReads', methods=['GET','POST'])
def viewsamplereads():
	return render_template('ViewSampleReads.html')


#******************************************************************************
# BEGIN: Share Project
#******************************************************************************

@app.route('/ShareProject', methods=['GET','POST'])
def ShareProject():
	try:
		data = request.get_json()
		users=data['users']
		pid=data['pid']
		for uname in users:
			try:
				uid=query_db('select * from user where user_affiliation="'+uname+'"')[0]['user_id']
				g.db.execute('INSERT INTO user_projects VALUES (?,?)', (uid,pid))
			except:
				pass
		g.db.commit()
		return 'success'
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: Make Project Public
#******************************************************************************

@app.route('/MakeProjectPublic', methods=['GET','POST'])
def MakeProjectPublic():
	try:
		data = request.get_json()
		users=data['users']
		pid=data['pid']
		for uname in users:
			try:
				uid=query_db('select * from user where user_affiliation="'+uname+'"')[0]['user_id']
				g.db.execute('INSERT INTO user_projects VALUES (?,?)', (uid,pid))
			except:
				pass
		g.db.commit()
		return 'success'
	except Exception as inst:
		return "ERROR: "+str(inst)





#******************************************************************************
# BEGIN: Get the one sample function data
#******************************************************************************
from app.lib.logs.breakdown import assembly, matches

@app.route('/breakdown', methods=['GET','POST'])
def breakdown():
	try:
		data = request.get_json()
		if data['pip']=='assembly':
			l1=assembly(data)
		else:
			l1=matches(data)
		return jsonify(matrix=l1)
	except Exception as inst:
		return "ERROR: "+str(inst)













#******************************************************************************
# BEGIN: get tree
#******************************************************************************

@app.route('/get_tree', methods=['GET','POST'])
def get_tree():
	try:
		data = request.get_json()
		pid=data["pid"]
		uid=data["uid"]
		sid=data["sid"]
		selval=data["value"]
		pipeline=data["pip"]
		dbname=data["rid"]
		#dbname="isuezrouja"
		analysis="taxonomy"
		rf=rootvar.result_files(pid,analysis,pipeline,sid,dbname)
		x=sql.SQL(main_db)
		samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
		xpath=x.project(pid)[0][4]
		sample=rootvar.samples(samples[0],xpath)
		with open(rf.json) as data_file:
			data = json.load(data_file)
		x.close()
		###print data
		view=rootvar.ViewSampleResults(sample,pipeline, dbname, analysis, rf)
		return jsonify(tree=[data], range=view.range(selval)[0], pip=pipeline)
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: get taxo
#******************************************************************************

@app.route('/get_taxo_by_name', methods=['GET','POST'])
def get_taxo_by_name():
	data = request.get_json()
	pid=data["pid"]
	uid=data["uid"]
	sid=data["sid"]
	tid=data["tid"]
	lid=data["lid"]
	pip=data["pip"]
	dbname=data["rid"]
	pipeline=pip
	#dbname="isuezrouja"
	analysis="taxonomy"
	x=sql.SQL(main_db)
	rf=rootvar.result_files(pid,analysis,pip,sid,dbname)
	samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
	xpath=x.project(pid)[0][4]
	sample=rootvar.samples(samples[0],xpath)
	x.close()
	view=rootvar.ViewSampleResults(sample,pipeline,dbname,analysis, rf)
	try:
		#return jsonify(x=pip)
		return jsonify(matrix=view.level(lid,type="matches"))
	except Exception as inst:
		return "ERROR: "+str(inst)


#******************************************************************************
# BEGIN: when click on the node tree
#******************************************************************************

@app.route('/get_childs_of_taxonomy', methods=['GET','POST'])
def get_childs_of_taxonomy():
    data = request.get_json()
    pid=data["pid"]
    uid=data["uid"]
    sid=data["sid"]
    tid=data["tid"]
    lid=data["lid"]
    cond=data["cond"]
    pip=data["pip"]
    rid=data["rid"]

    dbname=data["rid"]
    analysis="taxonomy"

    ##print cond, pip, rid, pid, uid, sid, tid, lid


    if cond=="one": # this is if I am analyzing one or multiple samples
        rf=rootvar.result_files(pid,analysis,pip,sid,dbname)
        x=sql.SQL(main_db)
        samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
        xpath=x.project(pid)[0][4]
        sample=rootvar.samples(samples[0],xpath)
        x.close()
        view=rootvar.ViewSampleResults(sample,pip,dbname,analysis,rf)
        matrix=view.childs_of(tid,'rpkm')
        ###print matrix
        return jsonify(matrix=matrix)
    else:
        # load big tree
        all_samples_tree_file=rootvar.__ROOTPRO__+"/"+pid+"/"+pip+"/RESULTS/"+rid+".all_samples_tree.pk"
        G=nx.read_gpickle(all_samples_tree_file)
        tree=json_graph.tree_data(G,root='R')
        data=[]
        for i in G.successors(tid):
            data.append(i)
        x=sql.SQL(all_samples_tree_file+".db")


        matrix=rootvar.get_matrix_level_childs(x,data)
        samples_sel=list(set([str(i[0]) for i in matrix]))
        M,N=rootvar.v2m(matrix,samples_sel,0,0)
        ##print M
        heatmap='none' #heatmap=iclust.main(M,None)
        return jsonify(data=matrix[0], heatmap=heatmap)

#******************************************************************************
# BEGIN: get statistics
#******************************************************************************

def statsP(sample,program,sid,ndb,pipeline):
    if pipeline=="matches":
        path=sample.matchesDir
    else:
        path=sample.assemblyDir
    if program == "flash":
        file=path+"flash.log"
        fs=[]
        with open(file) as f:
            for i in f:
                fs.append(" ".join(i.split()[1:]))
        return([fs[-7],fs[-6],fs[-10],fs[-11]])
    if program == "bowtie":
        file=path+"/alignment."+ndb+".log"
        fs=[]
        with open(file) as f:
            for i in f:
                fs.append(i.replace("\n",""))
        return([fs[-1],fs[-2],fs[-3],fs[-4]])


@app.route('/get_statistics', methods=['GET','POST'])
def get_statistics():
    data = request.get_json()
    pid=data["pid"]
    uid=data["uid"]
    sid=data["sid"]
    programs=data["value"]
    dbname="isuezrouja"

    x=sql.SQL(main_db)
    samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
    xpath=x.project(pid)[0][4]
    pname=str(x.project(pid)[0][1])
    ##print pname
    sample=rootvar.samples(samples[0],xpath)
    x.close()
    ###print matrix
    data=[]
    pipeline="matches"
    for program in programs:
        data.append(statsP(sample,program,sid,dbname,pipeline))
    return jsonify(stats=data,sname=sample.name, pname=pname)






#******************************************************************************
# BEGIN: Get the one sample function data
#******************************************************************************
from app.lib.logs.logs import assembly as logassembly
@app.route('/get_assembly_logs', methods=['GET','POST'])
def get_assembly_logs():
	try:
		data = request.get_json()
		pid = data["pid"]
		uid = data["uid"]
		sid = data["sid"]
		pip = data["pip"]
		analysis = "function"
		lid = "assembly"
		#file=rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/pred.genes."+rid+".matches.function.abundance.results.sqlite3.db"
		if lid=="assembly":
			l1=logassembly(rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/")
		return jsonify(matrix=l1)
	except Exception as inst:
		return "ERROR: "+str(inst)

from app.lib.logs.logs import matches as logmatches
@app.route('/get_matches_logs', methods=['GET','POST'])
def get_matches_logs():
	try:
		data = request.get_json()
		pid=data["pid"]
		sid=data["sid"]
		li=logmatches(rootvar.__ROOTPRO__+"/"+pid+"/READS/"+sid+"trim.log")
		return jsonify(matrix=li)
	except Exception as inst:
		return "ERROR: "+str(inst)




#******************************************************************************
# Download FILES
#******************************************************************************
from flask import send_file
@app.route("/download/<file_name>")
def getFile(file_name):
	#return base64.b64decode(file_name)
	try:
		return send_file(base64.b64decode(file_name), as_attachment=True)
	except Exception as inst:
		return str(inst)




































#******************************************************************************
# BEGIN: Get the one sample function data
#******************************************************************************
@app.route('/get_functional_counts', methods=['GET','POST'])
def get_functional_counts():
	try:
		data = request.get_json()
		pid=data["pid"]
		uid=data["uid"]
		sid=data["sid"]
		pip=data["pip"]
		rid=data["rid"]
		pip=data['pip']
		analysis="function"
		#lid="assembly"
		#file=rootvar.__ROOTPRO__+"/"+pid+"/assembly/idba_ud/"+sid+"/pred.genes."+rid+".matches.function.abundance.results.sqlite3.db"
		x=sql.SQL(main_db)
		rf=rootvar.result_files(pid,"function",pip,sid,rid)
		samples=x.exe('select * from samples where project_id="'+pid+'" and sample_id="'+sid+'"')
		xpath=x.project(pid)[0][4]
		sample=rootvar.samples(samples[0],xpath)
		x.close()
		view=rootvar.ViewSampleResults(sample,pip,rid,analysis, rf)
		return jsonify(matrix=view.func_one_sample(), m2=view.func_structure(pid,pip,sid))
	except Exception as inst:
		return "ERROR: "+str(inst)









































#******************************************************************************
# BEGIN: Compare samples`
#******************************************************************************
@app.route('/compare_samples', methods=['GET','POST'])
def compare_samples():
    pid = request.args.get('pid', "None", type=str)
    ##print pid
    return render_template('compare_samples.html')

#******************************************************************************
# BEGIN: get all samples and tree
#******************************************************************************

def format_matrix(P):
	for i,vec in enumerate(P):
		for j,pos in enumerate(vec):
			try:
				P[i][j]=round(float(pos),5)
			except:
				pass
	return P

def format_matrix_ht(Q, description):
	header=Q[0]
	data={}
	for ix, i in enumerate(Q):
		data.setdefault("data",[]).append({str(header[jx]):j for jx,j in enumerate(i)})
	return data['data']

def process_matrix_vis(N, ie, ib):
	O=np.delete(N[1:], 0, 1)
	O=np.sum(np.array(O, dtype='float'),axis=0)
	idx = O.argsort()+1
	if ie>len(idx): ie=len(idx)
	idx=idx[::-1][ib:ie]
	idx=np.insert(idx, 0, 0)
	P=np.take(N, idx, axis=1).tolist()
	return format_matrix(P)


from app.lib.main_func import get_all_samples_tree as GetSamplesTree
from app.lib.inchlib import inchlib_clust as IL
#import app.lib.inchlib.inchlib_clust as IL
#import sklearn
@app.route('/get_all_samples_tree', methods=['GET','POST'])
def get_all_samples_tree():
	try:
		data = request.get_json()

		X=GetSamplesTree.run(data)
		# return "step 2"

		minA=data['minA']
		if data['norm']=="scale":
			nzt=1
		elif data['norm']=='rpkm':
			nzt=0
		elif data['norm']=='16s':
			nzt=2

		try:
			ib=data['ib']-1; ie=data['ie'];
		except:
			ib=0; ie=10;
		#b=0; e=10
		###print minA

		try:
			db_desc=json.load(open(rootvar.__ROOTDBS__+"/"+data['rid']+"/dataset.description.json"))
		except:
			db_desc=False

		if X[0]=='taxonomy':
			tree=X[1]
			matrix=rootvar.get_matrix_level(data,data["lid"])

			#return jsonify(x=matrix)
			samples_sel=data["snames"]#list(set([str(i[0]) for i in matrix]))
			M,N=rootvar.v2m(matrix,samples_sel,nzt,0) # N is not log2 transformed, M its id
			P=process_matrix_vis(N, ie, ib)
			m2js=map(list, zip(*P))
			tmp=m2js[1:]
			tmp.sort(key=lambda x: float(x[1]+x[2]) , reverse=True)
			heatmap=IL.main(m2js,None)
			return jsonify(tree=[tree], heatmap=heatmap[0], aid="taxonomy", matrix=[m2js[0]]+tmp, N=heatmap[1])
		elif X[0]=='function':
			samples_sel=data["snames"]#list(set([str(i[0]) for i in X[1]]))
			# this function converts a python vector into a matrix like structure.
			###print "making a square matrix!", len(X[1]),len(X[1][0])
			M,N=rootvar.v2m(X[1],samples_sel,nzt,0)
			#return jsonify(N=N, X=X[1], s=samples_sel)
			P=process_matrix_vis(N, ie, ib)
			Q=format_matrix_ht(format_matrix(np.transpose(P).tolist()), db_desc)

			for ix,i in enumerate(Q):
				try:
					Q[ix]['description']=db_desc[i['samples']]['X1'].replace('"',"")
				except:
					Q[ix]['description']='Function'
				try:
					Q[ix]['Long_Description']=db_desc[i['samples']]['X2'].replace('"',"")
				except:
					Q[ix]['Long_Description']='Description'


			m2js=map(list, zip(*P))
			heatmap=IL.main(m2js,None)
			tmp=m2js[1:]
			tmp.sort(key=lambda x: float(x[1]+x[2]) , reverse=True)

			return(jsonify(aid="function",heatmap=heatmap[0],matrix=[m2js[0]]+tmp, table=Q, samples=samples_sel))
	except Exception as inst:
		return "ERROR: "+str(inst)



################ GET MULTIPLE PROJECTS #################





@app.route('/get_multiple_projects', methods=['GET','POST'])
def get_multiple_projects():
	try:
		data = request.get_json()
		M=[]
		for pid in data['pids']:

			data['pid']=pid

			samples_sel=data["snames"]
			X=GetSamplesTree.run(data)
			if data['norm']=="scale":
				nzt=1
			elif data['norm']=='rpkm':
				nzt=0
			elif data['norm']=='16s':
				nzt=2
			try:
				ib=data['ib']-1; ie=data['ie'];
			except:
				ib=0; ie=10;

			if X[0]=='taxonomy':
				matrix=[[pid+":"+i[0], i[1], i[2], i[3]] for i in rootvar.get_matrix_level(data,data["lid"])]
			elif X[0]=='function':
				matrix=[[pid+":"+i[0], i[1], i[2], i[3]] for i in X[1]]
			M+=matrix

		M,N=rootvar.v2m(M,samples_sel,0,0)
		P=process_matrix_vis(N, ie, ib)
		m2js=map(list, zip(*P))
		tmp=m2js[1:]
		#tmp.sort(key=lambda x: float(x[1]+x[2]) , reverse=True)
		heatmap=IL.main(m2js,None)
		heatmap[0]['data']['feature_names']=order=[i.split(":")[1] for i in heatmap[0]['data']['feature_names']]

		return jsonify(matrix=[m2js[0]]+tmp, heatmap=heatmap[0], P=P)
	except Exception as inst:
		return "ERROR: "+str(inst)









################ NETWORK ANALYSIS #################
@app.route('/network', methods=['GET','POST'])
def network():
	try:
		data=request.get_json()
		pid = request.args.get('pid', "None", type=str)
		return render_template('/network/network.html',output=str(data))
	except Exception as inst:
		render_template('/network/network.html',output=str(inst))




################ DOWNLOAD FILES #################
from app.lib.common.arc_connect import bench2archu, arcon

@app.route('/download_files', methods=['GET','POST'])
def download_files():
	try:
		data=request.get_json()
		fi =  data['file']
		uid = data['uid']
		sid = data['sid']
		pid = data['pid']
		fnm = data['name']

		os.system('mkdir /home/raid/www/MetaStorm/main/tmp/'+sid+"/")
		scp=arcon()

		scp.get(fi, '/home/raid/www/MetaStorm/main/tmp/'+sid+"/"+fnm)

		return jsonify(fo = '/home/raid/www/MetaStorm/main/tmp/'+sid+"/"+fnm)
	except Exception as inst:
		return str(inst)





























































































































































































#******************************************************************************
# Compare projects
#******************************************************************************

@app.route('/compare_projects',methods=['GET','POST'])
def compare_projects():
	try:
		#data = request.get_json()
		#projects = data['pid']
		return render_template('compare_projects.html')
	except Exception as inst:
		return "ERROR: "+str(inst)


@app.route('/compare_projects_1',methods=['GET','POST'])
def compare_projects_1():
	try:
		data = request.get_json()
		projects = data['pid']
		return 'ok'
	except Exception as inst:
		return "ERROR: "+str(inst)























#******************************************************************************
# SEND email from javascript
#******************************************************************************

@app.route('/sendEmail',methods=['GET','POST'])
def sendEmail():
	try:
		data = request.get_json()
		message=data['msg']
		uid=data['uid']
		if uid=="TesREPDooc73Ohw": return 'User not allowed'
		subject=data['sub']
		S=query_db('select * from user where user_id="'+uid+'"')
		x=email.send_email(S[0]['user_name'],S[0]['user_affiliation'],subject,message)
		return "success"
	except Exception as inst:
		return "ERROR: "+str(inst)












@app.route('/')
def index():
	return render_template('index.html')


@app.route('/index5')
def nindex():
	return render_template('index5.html')

@app.route('/visualization')
def visualizationR():
	return render_template('visualization.html')





@app.route('/TaxonomyTree')
def TaxonomyHTML():
	return render_template('TaxonomyTree.html')


@app.route('/status/')
def jobstatus():
    	return 0


if __name__ == '__main__':
	app.run(debug=True)
