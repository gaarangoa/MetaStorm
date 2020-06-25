FROM python:2.7.15

RUN pip install --upgrade pip 
RUN pip install flask==1.0.2
RUN pip install pymongo==3.7.2
RUN pip install flask_cors==3.0.6
RUN pip install requests==2.18.4
RUN pip install numpy==1.15.4
RUN pip install networkx==1.11
RUN pip install scikit-learn==0.20.3
RUN pip install biopython==1.73
RUN pip install paramiko==2.4.2
RUN pip install scp==0.13.2
RUN pip install fastcluster==1.1.25


