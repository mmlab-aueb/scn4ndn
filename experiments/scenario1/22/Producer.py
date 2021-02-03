from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
import os
import json
#nfdc face create udp://ndn.netsec.colostate.edu

face = "udp://ndn.netsec.colostate.edu"
#face = "udp://mmlab-aueb-1.mmlab.edu.gr"
#face = "udp://titan.cs.memphis.edu"

prefix = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com"

app = NDNApp()
cert = app.keychain[prefix].default_key().default_cert()

print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /localhop/nfd ' + face)

file1_metadata={
    'chunks': 10,
    'alsoknownas':'/ndn/edu/colostate/%40GUEST/nikosft%40gmail.com/file1' 
}

print("Will adverise:" + Name.to_str(cert.key))
@app.route(cert.key)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for key")
    app.put_raw_packet(cert.data)

print("Will adverise:" + prefix + '/file1')
@app.route(prefix + '/file1')
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for " + Name.to_str(name))
    chunk =  Component.to_str(name[-1])
    if (chunk == 'file1'):
        app.put_data(name, content=json.dumps(file1_metadata).encode(), freshness_period=1)
    else:
        data = 'File1/' + chunk
        app.put_data(name, content=data.encode() , freshness_period=1)
   

if __name__ == '__main__':
    app.run_forever()
