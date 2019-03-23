FROM python:2.7
RUN pip install flask
RUN pip install pymongo
RUN pip install flask_cors
RUN pip install requests
RUN pip install numpy
RUN pip install networkx
RUN pip install sklearn
RUN pip install biopython
RUN pip install paramiko
RUN pip install scp
RUN pip install fastcluster

# the first time creating the container you have to:
# RUN docker exec -it metastorm_backend_1 bash
# RUN ssh-keygen -t rsa -b 2048 -v -N "" -f /root/.ssh/id_rsa
# RUN ssh-copy-id -i /root/.ssh/id_rsa gustavo1@newriver1.arc.vt.edu

