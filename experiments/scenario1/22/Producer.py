from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import os
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



print("Will adverise:" + Name.to_str(cert.key))
@app.route(cert.key)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for key")
    app.put_raw_packet(cert.data)

print("Will adverise:" + prefix + '/file1')
@app.route(prefix + '/file1')
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for " + Name.to_str(name))
    app.put_data(name, content=b'Info about scn4ndn from .22', freshness_period=10000)
   

if __name__ == '__main__':
    app.run_forever()
