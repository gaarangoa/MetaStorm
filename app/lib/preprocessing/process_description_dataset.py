import json


x=open('dataset.description').readlines()

headers=x[0].replace('\n',"").split('\t')

idheaders=['X'+str(i) for i in range(len(headers))]

data={}
for line in x[1:]:
    line=line.strip().split("\t")
    data[line[0]]={idheaders[i]:j for i,j in enumerate(line)}

json.dump(data,open('dataset.description.json', 'w'))

