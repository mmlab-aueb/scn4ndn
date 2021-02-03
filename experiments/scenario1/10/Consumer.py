from ndn.encoding import Name
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

import os

face = "udp://mmlab-aueb-1.mmlab.edu.gr"

print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /ndn ' + face)
app = NDNApp()

def data_received(insterest_name, data_name, meta_info, content):
    # Print out Data Name, MetaInfo and its conetnt.
    print(f'Received Data Name: {Name.to_str(data_name)}')
    print(meta_info)
    print(bytes(content) if content else None)

def interest_failed(interest_name):
    printf(interest_name + " Failed")


async def express_interest(insterest_name):
    try:
        prefix = "/ndn/edu/colostate/%40GUEST/nikosft%40gmail.com"
        data_name, meta_info, content = await app.express_interest(
            insterest_name,
            must_be_fresh=False,
            can_be_prefix=True,
            lifetime=6000)
        data_received(insterest_name, data_name, meta_info, content)
    except (InterestNack, InterestTimeout, InterestCanceled, ValidationFailure) as e:
        interest_failed(insterest_name)

def run():
    interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/about"
    express_interest(interest_name)
    #app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=run())
