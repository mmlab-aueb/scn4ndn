
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo
from ndn.transport.stream_socket import UnixFace

app= NDNApp()

@app.route('/scn4ndn/testApp')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=b'content', freshness_period=10000)


if __name__ == '__main__':
    app.run_forever()
