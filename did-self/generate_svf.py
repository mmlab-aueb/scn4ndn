'''
It generates a self-verified file
Usage:
> python3 generate_svf.py <input-file> <key file> <did-document file>

Notes:
* It does not make any check in the did-document file, it assumes it is correct!
* It loads the whole file in the memory, make sure that the file is small!
'''
import hashlib
import sys
import json
from jwcrypto import jwk, jws

if (len(sys.argv) != 4):
    print("Usage: generate_svf.py <input-file> <key file> <did-document file>")
    exit()

with open(sys.argv[1], 'r') as _file:
    input_file = _file.read()

with open(sys.argv[2], 'r') as _file:
    key_dict = json.load(_file)

with open(sys.argv[3], 'r') as _file:
    doc_dict = json.load(_file)

sha256 = hashlib.sha256() 
sha256.update(input_file.encode())
metadata = {
    'name':doc_dict['document']['id'].split(":")[2],
    'sha-256':sha256.hexdigest()
}
key = jwk.JWK(**key_dict)
jws_payload = json.dumps(metadata)
proof = jws.JWS(jws_payload.encode('utf-8'))
proof.add_signature(key, None, json.dumps({"alg": "EdDSA"}),None)
proof.objects['payload']=''
header = json.dumps([doc_dict, metadata, proof.serialize(compact=True)])

with open(metadata['name']+'.svf', 'w') as _file:
    _file.write(header)
    _file.write('\n')
    _file.write(input_file)

