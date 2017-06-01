import os
import subprocess
from app.lib.common import rootvar

__ROOTEXEDIR__=rootvar.__ROOTEXEDIR__#="/home/zhanglab/public_html/software/CMetAnn/Files/bin/"
#__chimeraDB__="/research/gustavo1/Dropbox/PhDProjects/metagenomics/MetaGen/Files/REFERENCE/chimera/gold.udb"

def mkdir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

class trimmomatic:
	def __init__(self,m1,m2,outdir,sample_id):
		self.mate1=m1
		self.mate2=m2
		self.sid=sample_id
		self.exe="java -jar "+__ROOTEXEDIR__+"/trimmomatic-0.33.jar"
		self.options="PE -phred33"
		self.outd=outdir+"/"
		self.om1 = self.mate1+'.fq'
		self.om2 = self.mate2+'.fq'
		self.cmd =" ".join([self.exe, self.options, self.mate1, self.mate2, self.om1, self.mate1+".unpaired.fq.gz", self.om2, self.mate2+".unpaired.fq.gz", "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 >> ", self.outd+self.sid+'trim.log', "2>&1"])
	def run(self):
		mkdir(self.outd)
		try:
			os.system(self.cmd)
			os.system("mv "+self.om1+" "+self.mate1.replace(".gz",""))
			os.system("mv "+self.om2+" "+self.mate2.replace(".gz",""))
			#os.system("echo success >"+self.outd+self.sid+'trim.log')
		except: pass

class flash:
	def __init__(self, m1, m2, outdir):
		self.exe=__ROOTEXEDIR__+"/flash"
		self.options="--allow-outies -M 500"
		self.log=">>"+outdir+"flash.log 2>&1"
		self.fout=outdir+"/flash.extendedFrags.fastq"
		self.cmd= " ".join([self.exe, self.options, '-d', outdir, "-o", "flash", m1, m2, self.log])
	def run(self):
		os.system(self.cmd)

class ffastq:
	def __init__(self, fin, sid, outdir):
		self.exe="split_libraries_fastq.py "
		self.opts=""
		self.fin=fin
		self.fout=outdir+"seqs.fna"
		self.sid=sid
		self.cmd1=__ROOTEXEDIR__+'/seqtk seq -a '+self.fin+'>'+self.fin+'.fasta'
		self.cmd2='awk -v tag="'+self.sid+'" '+''' '{if($_~/^>/){print ">"tag"_"i++}else{print}}' ''' +self.fin + '.fasta >' + self.fout
		#self.cmd=" ".join([self.exe,"-i",self.fin, '--sample ', sid, " --phred_offset 33  --barcode_type 'not-barcoded' -q 20 -o",outdir])
	def run(self):
		os.system(self.cmd1)
		os.system(self.cmd2)

class chimera:
	def __init__(self, fin, outf):
		self.exe=__ROOTEXEDIR__+"/usearch -usearch_global"
		self.cmd= " ".join([self.exe, fin, '-db', __chimeraDB__ ,"-id 0.9 -strand both", "-alnout", outf])
	def run(self):
		os.system(self.cmd)


class pick_rep_set:
	def __init__(self, otu, fasta):
		self.exe="pick_rep_set.py "
		self.cmd=" ".join([self.exe, '-i', otu, '-f', fasta])
	def run(self):
		os.system(self.cmd)


def assign_taxonomy():
	def __init__(self, fin):
		self.exe=""
