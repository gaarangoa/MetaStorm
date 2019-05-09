FROM python:2.7.5
RUN pip install flask
RUN pip install pymongo
RUN pip install flask_cors
RUN pip install requests
RUN pip install numpy
RUN pip install networkx==1.11
RUN pip install sklearn
RUN pip install biopython
RUN pip install paramiko
RUN pip install scp
RUN pip install fastcluster


