# About
These are instructions for connecting to the [NDN testbed](https://named-data.net/ndn-testbed/policies-connecting-nodes-ndn-testbed/) and registering a content prefix. 

## Prerequisites
Install the [https://named-data.net/doc/NFD/current/](https://named-data.net/doc/NFD/current/) in a
machine with Internet reachable IP address. Make sure that ports 6363 (TCP and UDP) and 9696 (TCP and UDP)
are open. We provide a Producer script that registers the appropriate digital certificate name and the desired content prefix. 
The Producer script is implemented in Python 3 and the [python-ndn](https://github.com/named-data/python-ndn)
library. You can install it using pip3 `pip3 install python-ndn`.

Use [NDN Certification System](https://ndncert.named-data.net) to receive a digital certificate and install
by following the provided instructions. 

## Preparation
Start NFD daemon (`nfd-start`). Select the NDN testbed node to which you wish to attach. You can find available
testbed nodes from the [NDN Testbed Status page](http://ndndemo.arl.wustl.edu). You can connect to any testbed
node. Suppose you select [mmlab-1 node](https://mmlab-aueb-1.mmlab.edu.gr/n/#tab=Overview), issue the following
commands

* nfdc face create udp://mmlab-aueb-1.mmlab.edu.gr
* nfdc route add /localhop/nfd udp://mmlab-aueb-1.mmlab.edu.gr 

With the first command you are creating a face towards node mmlab-1, whereas with the second command you are denoting
that mmlab-1 is your gateway and hence, all prefix registrations are forwarded to this node. 

## Execution
In the Producer.py script replace the `prefix` variable with the prefix for which you have generated the certificate.
Then execute the Producer script by invoking `python3 Producer.py`

### The Producer.py script
The following piece of code retrieves the certificate that corresponds to your prefix from the local keychain, it registers
its name, and when requested it sends the certificate. 

```python
cert = app.keychain[prefix].default_key().default_cert()
@app.route(cert.key)
def cert_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=cert.data, freshness_period=10000)
```

The following piece of code registers a content item name and when requested it send the corresponding data. 

```python
@app.route(prefix + 'info')
def info_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
    app.put_data(name, content=b'Info about scn4ndn', freshness_period=10000)
```
