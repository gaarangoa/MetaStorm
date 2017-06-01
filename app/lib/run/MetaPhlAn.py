
class MetaPhlAn:
    def __init__(self,input,output):
         self.input=input
         self.output=output







metaphlan2.py --input_type fasta --mpa_pkl ./db_v20/mpa_v20_m200.pkl --bowtie2db ./db_v20/mpa_v20_m200 -o profiled_metagenome.txt /research/gustavo1/Dropbox/PhDProjects/metagenomics/simulated_M_reads/in-silico/100bp.fa

../../../../../bin/metaphlan2/metaphlan2.py --input_type fasta --mpa_pkl ../../../../../bin/metaphlan2/db_v20/mpa_v20_m200.pkl --bowtie2db ../../../../../bin/metaphlan2/db_v20/mpa_v20_m200 -t rel_ab_w_read_stats --nproc 8  -o genes.metaphlan pred.genes.nucl.fa
