from ndn.encoding import Name
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

import os

face = "udp://mmlab-aueb-1.mmlab.edu.gr"

print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /ndn ' + face)
app = NDNApp()

async def main():
    try:
        prefix = "/ndn/edu/colostate/%40GUEST/nikosft%40gmail.com"
        data_name, meta_info, content = await app.express_interest(
            # Interest Name
            prefix + '/about',
            must_be_fresh=False,
            can_be_prefix=True,
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

    try:
        prefix = "/ndn/gr/aueb/thomasi"
        data_name, meta_info, content = await app.express_interest(
            # Interest Name
            prefix + '/about',
            must_be_fresh=False,
            can_be_prefix=True,
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
