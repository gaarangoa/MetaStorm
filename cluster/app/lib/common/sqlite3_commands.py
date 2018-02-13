from app.lib.create_project import insert_new_project as sql

def update_status(x,sid,rid,pip,status):
    val=x.exe("INSERT or REPLACE into sample_status(id,sid,rid,pip,status) values("+"'"+sid+"_"+rid+"_"+pip+"','"+sid+"','"+rid+"','"+pip+"','"+status+"')")
    x.commit()

def update_jobs(x,value):
    parameters="'"+"','".join(value)+"'"
    val=x.exe("INSERT or REPLACE into jobs(uid,pid,sid,pip,parameters,status,priority,date) values("+parameters+")")
    x.commit()
    
def update_number_jobs(x,priority,njobs):
    val=x.exe("INSERT or REPLACE into number_jobs(priority,jobs) values('"+priority+"',"+str(njobs)+")")
    x.commit()