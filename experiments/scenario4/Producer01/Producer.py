from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
import os

face = "udp://ndn.netsec.colostate.edu"
prefix = "/ndn/gr/edu/mmlab1/%40GUEST/fotiou%40aueb.gr"
print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /localhop/nfd ' + face)

app = NDNApp()
cert = app.keychain[prefix].default_key().default_cert()

print("Will adverise:" + Name.to_str(cert.key))
@app.route(cert.key)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for key")
    app.put_raw_packet(cert.data)

print("Will adverise:" + prefix)
@app.route(prefix)
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for " + Name.to_str(name))
   

if __name__ == '__main__':
    app.run_forever()
