from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
import os

face = "udp://ndn.netsec.colostate.edu"
#prefix = '/ndn/gr/edu/mmlab1/%40GUEST/fotiou%40aueb.gr'
#prefix = "/ndn/gr/aueb/fotiou"
prefix = "/ndn/edu/colostate/%40GUEST/fotiou%40aueb.gr"

print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /localhop/nfd ' + face)

app = NDNApp()
cert = app.keychain[prefix].default_key().default_cert()
print("Will adverise:" + Name.to_str(cert.key))

@app.route(cert.key)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for key")
    app.put_data(name, content=cert.data, freshness_period=10000)

print("Will adverise:" + prefix + '/info')
@app.route(prefix + '/info')
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest for /info")
    app.put_data(name, content=b'Info about scn4ndn from .14', freshness_period=10000)
   

if __name__ == '__main__':
    app.run_forever()