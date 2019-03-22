FROM python:2.7
RUN pip install flask
RUN pip install pymongo
RUN pip install flask_cors
RUN pip install requests
RUN pip install numpy

ENTRYPOINT ["python", "/main/run.py"]