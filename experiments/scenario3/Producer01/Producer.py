from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
import os
import json

face = "udp://ndn.netsec.colostate.edu"
prefix = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com"
print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /localhop/nfd ' + face)

app = NDNApp()
cert = app.keychain[prefix].default_key().default_cert()
file1_metadata={
    'chunks': 10,
    'alsoknownas':'/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/file2' 
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
        data = 'file1, chunk' + chunk
        app.put_data(name, content=data.encode() , freshness_period=100)
   
print("Will adverise:" + prefix + '/file2')
@app.route(prefix + '/file2')
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for " + Name.to_str(name))
    chunk =  Component.to_str(name[-1])
    data = 'file1, chunk' + chunk
    app.put_data(name, content=data.encode() , freshness_period=100)

if __name__ == '__main__':
    app.run_forever()
