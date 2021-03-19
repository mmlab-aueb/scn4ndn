'''
It verifies a self-verified file
Usage:
> python3 verify_svf.py <input-file> <name>
> python3 verify_svf.py <input-file> <name> <output-file>
'''

import hashlib
import sys
import os
import json
from jwcrypto import jwk, jws
from didself import registry

if (len(sys.argv) != 3 and len(sys.argv) != 4 ):
    print("Usage: verify_svf.py <input-file> <name>")
    print("Usage: verify_svf.py <input-file> <name> <output-file>")
    exit(os.EX_USAGE)

with open(sys.argv[1], "r") as _file:
    _header = _file.readline()
    input_file = _file.read()

header = json.loads(_header)
doc_dict = header[0]
metadata = header[1]
_proof   = header[2]
proof = jws.JWS()
proof.deserialize(_proof)
proof.objects['payload'] = json.dumps(metadata)

###----Check if file name is included in the metadata and in the did document---
name = sys.argv[2]
if(metadata['name'] != name):
    exit(os.EX_DATAERR)

if(doc_dict['document']['id'].split(":")[2] != name):
    exit(os.EX_DATAERR)

###---Check the DID document
try:
    registry.DIDSelfRegistry().load(doc_dict['document'],doc_dict['proof_chain'])
except:
    print("error 1")
    exit(os.EX_DATAERR)

###---Check the metadata hash---
sha256 = hashlib.sha256() 
sha256.update(input_file.encode())
if(metadata['sha-256'] != sha256.hexdigest()):
    exit(os.EX_DATAERR)

###---Check the signature of the metadata---
key_dict = doc_dict['document']['assertion'][0]['publicKeyJwk']
key = jwk.JWK(**key_dict)
try:
    proof.verify(key)
except:
    exit(os.EX_DATAERR)

exit(os.EX_OK)

