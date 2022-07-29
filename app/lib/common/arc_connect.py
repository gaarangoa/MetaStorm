import paramiko, json, base64
from app.lib.inchlib import setup as st
from scp import SCPClient

def bench2archu(arg):
    #print arg
    #paramiko.util.log_to_file('paramiko.log')
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(base64.b64decode(st.htsk), 22, base64.b64decode(st.usx), base64.b64decode(st.hst), timeout=10)
    stdin, stdout, stderr = s.exec_command(arg)
    return {"out":stdout.read(),"error":stderr.read()}
    s.close()

def get(fromf, tof):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.load_system_host_keys()
    s.connect(base64.b64decode(st.htsk), 22, base64.b64decode(st.usx), base64.b64decode(st.hst), timeout=10)
    scp = SCPClient(s.get_transport())

    scp.get(fromf, tof)

class arcon:
    def __init__(self):
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.s.load_system_host_keys()
        self.s.connect(base64.b64decode(st.htsk), 22, base64.b64decode(st.usx), base64.b64decode(st.hst), timeout=10)
        self.scp = SCPClient(self.s.get_transport())
    def ssh(self, arg):
        stdin, stdout, stderr = self.s.exec_command(arg)
        return {"out":stdout.read(),"error":stderr.read()}
    def get(self, fromf, tof):
        self.scp.get(fromf, tof)
    def put(self, fromf, tof):
        self.scp.put(fromf, tof)
        
    
