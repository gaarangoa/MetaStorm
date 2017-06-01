m1="/research/gustavo1/Dropbox/PhDProjects/metagenomics/Xiao/rawreads/"#S2_R1.fastq"
sid,p1,p2=['S1',m1+'S1_R1.fastq',m1+'S1_R2.fastq']

root="/research/gustavo1/Dropbox/PhDProjects/metagenomics/Side_pipeline/test/"

out=root+"/samples/"
fn.mkdir(out)


flash=fn.flash(p1,p2,outd,sid)
flash.run()

fq=fn.ffastq(flash.fout, sid, trim.outd)
fq.run()

chimera=fn.chimera(fq.fout, fq.fout+".chim_filter.aln")
	#chimera.run()
