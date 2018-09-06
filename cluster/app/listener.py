import sys
import json
import base64
import os

inp = json.loads(base64.b64decode(sys.argv[1]))
data = inp[0]
refs = inp[1]
sid = inp[2]
uid = inp[3]
pip = inp[4]
USER = inp[6]
SAMPLE = inp[7]

os.system("".join([
    ' curl ',
    ' -X ',
    ' GET ',
    ' http://bench.cs.vt.edu/MetaStorm/status?',
    ' sid=' + sid + '&',
    'pip=' + pip + '&',
    'uid=' + uid + '&',
    'status=' + sys.argv[2]
]))
