from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo

prefix = "/ndn/gr/aueb/mmlab%40aueb.gr"

app = NDNApp()

cert = app.keychain[prefix].default_key().default_cert()
@app.route(cert.key)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=cert.data, freshness_period=10000)

@app.route(prefix + 'info')
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=b'Info about scn4ndn', freshness_period=10000)
   

if __name__ == '__main__':
    app.run_forever()