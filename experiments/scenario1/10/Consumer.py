from ndn.encoding import Name, Component
from ndn.app import NDNApp
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

import os
import json
import time
import asyncio
start_time = time.time()

face = "udp://mmlab-aueb-1.mmlab.edu.gr"

print("Configuring NFD...")
os.system('nfdc face create ' + face)
os.system('nfdc route add /ndn ' + face)
app = NDNApp()

async def data_received(interest_name, data_name, meta_info, content):
    # Print out Data Name, MetaInfo and its conetnt.
    #print(f'Received Data Name: {Name.to_str(data_name)}')
    #print(meta_info)
    #print(bytes(content) if content else None)
    chunk = Component.to_str(data_name[-1])
    if (chunk == "file1"): #root
        print ("Received root %s" %(time.time() - start_time))
        data = bytes(content)
        metadata = json.loads(data.decode())
        await download_chuncks(Name.to_str(data_name),metadata)

    else:
        print ("Received chunk %s" %(time.time() - start_time))
        print(bytes(content)) 

def interest_failed(interest_name):
    print(interest_name + " Failed")

async def download_chuncks (content_name, metadata):
     print("Will downolad "+ content_name)
     tasks = [
       download_chuncks_worker(content_name,1,5),
       download_chuncks_worker(content_name,6,10)
      ]
   
     await asyncio.wait(tasks)

async def download_chuncks_worker (content_name, first, last):
    for x in range(first,last+1):
        interest_name = content_name + "/chunk" + str(x)
        print(interest_name)
        data_name, meta_info, content = await express_interest(interest_name)
        print(bytes(content)) 

async def express_interest(insterest_name):
    try:
        loop = asyncio.new_event_loop()
        data_name, meta_info, content = await app.express_interest(
            insterest_name,
            must_be_fresh=True,
            can_be_prefix=True,
            lifetime=6000)
        return  data_name, meta_info, content
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

async def run():
    interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/file1"
    print ("Sending interest for root %s" %(time.time() - start_time))
    data_name, meta_info, content = await express_interest(interest_name)
    await data_received(interest_name, data_name, meta_info, content) 	
    #interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/nikosft%40gmail.com/file1/chunk1"
    #await express_interest(interest_name)
    app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=run())
