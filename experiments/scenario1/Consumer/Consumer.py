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

async def metadata_received(interest_name, data_name, meta_info, content):
    print (f'{time.time() - start_time} \t received metadata')
    data = bytes(content)
    metadata = json.loads(data.decode())
    tasks = [
        download_chuncks_worker(Name.to_str(data_name),1,5),
        download_chuncks_worker(metadata['alsoknownas'],6,10)
    ]
    await asyncio.wait(tasks)


async def download_chuncks_worker (content_name, first, last):
    for x in range(first,last+1):
        interest_name = content_name + "/chunk" + str(x)
        data_name, meta_info, content = await express_interest(interest_name)
        print (f'{time.time() - start_time} \t received {interest_name}')

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
    interest_name = "/ndn/gr/edu/mmlab1/%40GUEST/fotiou%40aueb.gr/file1"
    print (f'{time.time() - start_time} \t sending interest')
    data_name, meta_info, content = await express_interest(interest_name)
    await metadata_received(interest_name, data_name, meta_info, content) 	
    app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=run())
