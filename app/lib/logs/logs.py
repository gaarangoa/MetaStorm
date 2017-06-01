
import numpy as np

def assembly(file):
    logs=open(file+"log").readlines()
    reads=logs[1].split()[1]
    avgreads=logs[3].split()[1]
    sca=logs[-1].split()
    aligned_reads=int(logs[-4].split()[1])

    genes=open(file+"pred.genes.gff").readlines()

    ldist=[int(i.split()[4])-int(i.split()[3]) for i in genes if not '#' in i]


    return {'reads':int(reads)/2,'alreads':aligned_reads/2,'avgreads':int(avgreads), 'scaffolds':int(sca[1]), 'n50':int(sca[3]), 'maxScaff':int(sca[5]), 'avgScaff':int(sca[7]), 'totalScaffLen':int(sca[-1]), 'NumGenes':len(ldist), 'maxGeneLength':max(ldist), 'avgGene':int(np.mean(ldist))}


def matches(fi):
    for i in open(fi):
        if "Input Read Pairs:" in i:
                i=i.split()
                totalReads=int(i[6])
                notrimReads=int(i[3])
                break
    return {'rawReads':notrimReads, 'hqReads':totalReads}