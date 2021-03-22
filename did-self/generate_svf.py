'''
It generates a self-verified file
Usage:
> python3 generate_svf.py <input-file> <key file> <did-document file>
> python3 generate_svf.py <input-file>

Notes:
* It does not make any check in the did-document file, it assumes it is correct!
* It loads the whole file in the memory, make sure that the file is small!
'''
import hashlib
import sys
import json
import datetime
from jwcrypto import jwk, jws
from didself import registry
from didself.proof_chain import generate_proof
from didself.did_util import Ed25519_to_didkey

if (len(sys.argv) != 2 and len(sys.argv) != 4):
    print("Usage: generate_svf.py <input-file> <key file> <did-document file>")
    print("Usage: generate_svf.py <input-file>")
    exit()

with open(sys.argv[1], 'r') as _file:
    input_file = _file.read()

if (len(sys.argv) == 4):
    with open(sys.argv[2], 'r') as _file:
        key_dict = json.load(_file)
    with open(sys.argv[3], 'r') as _file:
        doc_dict = json.load(_file)
else:
    registry = registry.DIDSelfRegistry()
    did_key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
    did_key_dict = did_key.export_public(as_dict=True)
    # Generate the DID document
    did = "did:self:" + did_key_dict['x']
    controller = Ed25519_to_didkey(did_key_dict['x'])
    created = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z' #we should use the same timestamp for all documenets
    user_key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
    user_key_dict = user_key.export(as_dict=True)
    did_document = {
        'id': did,
        'controller': controller,
        'assertion': [{
            'id': did + '#key1',
            'type': "JsonWebKey2020",
            'publicKeyJwk': user_key_dict
        }],  
    }
    proof = generate_proof(did_document, did_key, created)
    registry.create(did_document, proof)
    document, proof_chain = registry.read()
    doc_dict = {'document':document, 'proof_chain':proof_chain}
    key_dict = user_key_dict


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

