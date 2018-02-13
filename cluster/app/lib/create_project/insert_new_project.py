import sqlite3 as sql

class SQL:
	def __init__(self,db):
		self.dbname=db
		self.conn=sql.connect(db)
		self.c=self.conn.cursor()
	def close(self):
		self.conn.close()
	def commit(self):
		self.conn.commit()
	def exe(self,value):
		return(self.c.execute(value).fetchall())
	def view(self,db):
		return(self.c.execute("select * from {v1}".format(v1=db)).fetchall())
	def project(self,pid):
		return(self.c.execute("select * from project where project_id=='{pid}'".format(pid=pid)).fetchall())
	def sample(self,pid,sid):
		return(self.c.execute('select * from samples where sample_id="'+str(sid)+'" and project_id="'+str(pid)+'"').fetchall())
	def samples(self,pid):
		return(self.c.execute('select * from samples where project_id="'+str(pid)+'"').fetchall())
	def drop(self,db):
		self.c.execute("drop table {v1}".format(v1=db))
	def get_max_id(self,table):
		max_id=self.c.execute("select max({v1}) from {v2}".format(v1=table+"_id", v2=table)).fetchall()[0][0]
		if max_id==None: max_id=1;
		else: max_id=max_id+1;
		return max_id
	### INSERT element to a table
	def insert(self,db,values):
		self.c.execute("insert into {db} values {values}".format(db=db,values=values))
		self.conn.commit()
	def names(self, table):
		cursor = self.c.execute('select * from ' +table+'')
		names = list(map(lambda x: x[0], cursor.description))
		return names
