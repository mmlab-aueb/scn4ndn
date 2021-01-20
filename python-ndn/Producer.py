from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo

app = NDNApp()
cert = app.keychain['/ndn/gr/edu/mmlab1/%40GUEST/fotiou%40aueb.gr'].default_key().default_cert()
print(Name.to_str(cert.key))

@app.route(cert.key)
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=cert.data, freshness_period=10000)

@app.route('/ndn/gr/edu/mmlab1/%40GUEST/fotiou%40aueb.gr/info')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=b'Info about scn4ndn', freshness_period=10000)
   

if __name__ == '__main__':
    app.run_forever()