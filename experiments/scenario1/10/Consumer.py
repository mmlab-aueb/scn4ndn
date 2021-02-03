from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

import os
import json

face = "udp://mmlab-aueb-1.mmlab.edu.gr"

print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /ndn ' + face)
app = NDNApp()

def data_received(insterest_name, data_name, meta_info, content):
    # Print out Data Name, MetaInfo and its conetnt.
    #print(f'Received Data Name: {Name.to_str(data_name)}')
    #print(meta_info)
    #print(bytes(content) if content else None)
    chunk = Component.to_str(data_name[-1])
    if (chunk == "file1"): #root
        data = bytes(content)
        metadata = json.loads(data.decode())
        print(metadata['chunks'])
    else:
        print(bytes(content)) 

def interest_failed(interest_name):
    print(interest_name + " Failed")


async def express_interest(insterest_name):
    try:
        prefix = "/ndn/edu/colostate/%40GUEST/nikosft%40gmail.com"
        data_name, meta_info, content = await app.express_interest(
            insterest_name,
            must_be_fresh=True,
            can_be_prefix=True,
            lifetime=6000)
        data_received(insterest_name, data_name, meta_info, content)
    except (InterestNack, InterestTimeout, InterestCanceled, ValidationFailure) as e:
        interest_failed(insterest_name)

async def run():
    interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/file1"
    await express_interest(interest_name)
    interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/file1/chunk1"
    await express_interest(interest_name)
    app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=run())
