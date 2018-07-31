FROM python
RUN pip install flask
RUN pip install pymongo
RUN pip install flask_cors
RUN pip install requests
RUN pip install numpy
RUN pip install sklearn
RUN pip install scipy
RUN pip install BioPython
RUN pip install paramiko
RUN pip install scp
RUN pip install fastcluster


ENTRYPOINT ["python", "/src/run.py"]