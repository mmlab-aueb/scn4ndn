
from typing import Optional
from ndn.app import NDNApp
from ndn.encoding import Name, InterestParam, BinaryStr, FormalName, MetaInfo, Component
from ndn.transport.stream_socket import UnixFace

app= NDNApp()

@app.route('/scn4ndn/testApp')
def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    print("Received interest")
    filename =  Component.to_str(name[-1])
    with open(filename + ".svf", 'r') as _file:
        content = _file.read()
        app.put_data(name, content=content.encode(), freshness_period=10000)


if __name__ == '__main__':
    app.run_forever()
