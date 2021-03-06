import os
import sys
from ndn.encoding import Name
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn.transport.stream_socket import UnixFace

#app = NDNApp(face=UnixFace(path="/run/h1.sock"))
#path = os.path.expanduser('~/.ndn/client.conf')
#print(path)
app = NDNApp()
async def main():
    try:
        data_name, meta_info, content = await app.express_interest(
            # Interest Name
            '/scn4ndn/testApp/GExt6UZsqMtIwYHaA2SCx7r5oSP0QSjIp2rTRUxuqYo',
            must_be_fresh=True,
            can_be_prefix=False,
            # Interest lifetime in ms
            lifetime=6000)
        # Print out Data Name, MetaInfo and its conetnt.
        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        print(bytes(content) if content else None)
    except InterestNack as e:
        # A NACK is received
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        # Interest times out
        print(f'Timeout')
    except InterestCanceled:
        # Connection to NFD is broken
        print(f'Canceled')
    except ValidationFailure:
        # Validation failure
        print(f'Data failed to validate')
    finally:
        app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=main())