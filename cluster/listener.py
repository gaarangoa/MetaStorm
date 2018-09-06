import sys
import json
import base64
import os

os.system(" ".join([
    ' curl ',
    ' --header "Content-Type: application/json"'
    ' --request POST',
    ' --data '+json.dumps({"job": sys.argv[1], "status": sys.argv[2]}),
    ' http://bench.cs.vt.edu/MetaStorm/status'
]))
