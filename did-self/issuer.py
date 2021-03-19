'''
It creates a number of JWK keys. It uses the first one
as the controller of a did:self DID and the rest as 
"assertion" verification methods
'''
from didself import registry
from didself.proof_chain import generate_proof
from didself.did_util import Ed25519_to_didkey
from jwcrypto import jwk
import datetime
import json

registry = registry.DIDSelfRegistry()
# DID creation
# Generate DID and initial secret key, it is also used as a controller
did_key = jwk.JWK.generate(kty='OKP', crv='Ed25519')
did_key_dict = did_key.export_public(as_dict=True)
# Generate the DID document
did = "did:self:" + did_key_dict['x']
controller = Ed25519_to_didkey(did_key_dict['x'])
created = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z' #we should use the same timestamp for all documenets
users = ['owner', 'cdn-1', 'cdn-2', 'cdn-3', 'cdn-4']
for user in users:
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
    did_doc = {'document':document, 'proof_chain':proof_chain}
    # dumping to file
    with open(user+'.key', 'w') as outfile:
        json.dump(user_key_dict, outfile)
    with open(user+'.document', 'w') as outfile:
        json.dump(did_doc, outfile)

