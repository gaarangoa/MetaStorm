import sys
import json
import os

os.system(" ".join([
    ' curl ',
    ' --header "Content-Type: application/json"'
    ' --request POST',
    ' --max-time 5',
    " --data '"+json.dumps({"job": sys.argv[1], "status": sys.argv[2]})+"'",
    ' http://bench.cs.vt.edu/MetaStorm/status'
]))
