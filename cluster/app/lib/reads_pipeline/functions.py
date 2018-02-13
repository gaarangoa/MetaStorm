import os

__ROOTEXEDIR__="/home/zhanglab/public_html/software/CMetAnn/Files/bin/"
#__chimeraDB__="/research/gustavo1/Dropbox/PhDProjects/metagenomics/MetaGen/Files/REFERENCE/chimera/gold.udb"

def mkdir(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

class trimmomatic:
	def __init__(self,m1,m2,outdir,sid):
		self.mate1=m1
		self.mate2=m2
		self.exe="java -jar "+__ROOTEXEDIR__+"/trimmomatic-0.33.jar"
		self.options="PE -phred33"
		self.outd=outdir+"/"+sid+"/"
		self.om1 = self.outd+"R1_paired.fq.gz"
		self.om2 = self.outd+"R2_paired.fq.gz"
		self.cmd =" ".join([self.exe, self.options, self.mate1, self.mate2, self.om1, self.outd+"R1_unpaired.fq.gz", self.om2, self.outd+"R2_unpaired.fq.gz", "ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36"])
	def run(self):
		mkdir(self.outd)
		os.system(self.cmd)

class flash:
	def __init__(self, m1, m2, outdir, sid):
		self.exe=__ROOTEXEDIR__+"/flash"
		self.options="--allow-outies -M 100"
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
		self.cmd=" ".join([self.exe,"-i",self.fin, '--sample ', sid, "--barcode_type 'not-barcoded' -q 20 -o",outdir])
	def run(self):
		os.system(self.cmd)

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
