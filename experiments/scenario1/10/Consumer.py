from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

import os
import json
import time
start_time = time.time()

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
        print ("Received root %s" %(time.time() - start_time))
        data = bytes(content)
        metadata = json.loads(data.decode())
        loop.run_until_complete(download_chuncks(metadata))
    else:
        print ("Received chunk %s" %(time.time() - start_time))
        print(bytes(content)) 

def interest_failed(interest_name):
    print(interest_name + " Failed")

async def download_chuncks (metadata):
    await asyncio.gather(
        download_chuncks(Name.to_str(data_name),metadata['chunks'])
    ) 

async def download_chuncks_worker (content_name, num_chunks):
    for x in num_chunks:
        insterest_name = content_name + "/chunk" + 1
        await express_interest(interest_name) 

async def express_interest(insterest_name):
    try:
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
    print ("Sending interest for root %s" %(time.time() - start_time))
    await express_interest(interest_name)
    interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/file1/chunk1"
    await express_interest(interest_name)
    app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=run())
