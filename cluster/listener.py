import sys
import json
import base64
import os

inp = json.loads(base64.b64decode(sys.argv[1]))


os.system(" ".join([
    ' curl ',
    ' --header "Content-Type: application/json"'
    ' --request POST',
    ' --data '+json.dumps({"job": sys.argv[1], "status":sys.arg[2]}),
    ' http://bench.cs.vt.edu/MetaStorm/status'
]))
