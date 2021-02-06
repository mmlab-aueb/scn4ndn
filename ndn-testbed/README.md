## Prerequisites

https://github.com/named-data/python-ndn

* pip3 install python-ndn

## Execution
(
* nfd-start (nfd --config /usr/local/etc/ndn/nfd.conf)
* nfdc face create udp://mmlab-aueb-1.mmlab.edu.gr (nfdc face create udp://ndn.netsec.colostate.edu)
* nfdc route add /localhop/nfd udp://mmlab-aueb-1.mmlab.edu.gr (nfdc route add /localhop/nfd udp://ndn.netsec.colostate.edu)
* python3 Producer.py
* python3 Consumer.py
* ndn6-serve-certs /home/scn4ndn/cert.ndncert
* ndnpingserver /ndn/gr/edu/mmlab1/%40GUEST/fotiou%40aueb.gr/test 
* ndnpingserver /ndn/gr/aueb/fotiou/test