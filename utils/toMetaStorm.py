import json

variant = {}
for i in open('protein_fasta_protein_variant_model.fasta'):
    if i[0] != ">": continue
    variant[i.split("|")[1]] = True

for i in open('protein_fasta_protein_overexpression_model.fasta'):
    if i[0] != ">": continue
    variant[i.split("|")[1]] = True

x = json.load(open('card.json'))

fa = open('dataset.fasta', 'w')
fu = open('dataset.func', 'w')
fd = open('dataset.description', 'w')

for model in x:
    try:
        for sequence in x[model]['model_sequences']['sequence']:
            protein = x[model]['model_sequences']['sequence'][sequence]['protein_sequence']
            # 
            try:
                assert(variant[protein['accession']])
            except:
                if not protein['accession'] == '':
                    fa.write('>'+protein['accession']+'\n'+protein['sequence']+'\n') 
                    fu.write(protein['accession']+"\t"+"-".join(x[model]['model_name'].split())+"\n")
                # 
                dsc = ''
                for aro in x[model]['ARO_category']:
                    dsc += x[model]['ARO_category'][aro]['category_aro_name']+";"
                # 
                fd.write("-".join(x[model]['model_name'].split())+"\t"+"-".join(dsc.split())+"\t"+"-".join(x[model]['ARO_description'].split())+"\n")
            # 
    except:
        pass

