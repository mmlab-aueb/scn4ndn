## Prerequisites

https://github.com/named-data/python-ndn

* pip3 install python-ndn

## Execution
(
* nfd-start (nfd --config /usr/local/etc/ndn/nfd.conf)
* nfdc face create udp://mmlab-aueb-1.mmlab.edu.gr/
* nfdc route add /ndn udp://mmlab-aueb-1.mmlab.edu.gr/
* nfdc route add /localhop/nfd udp://mmlab-aueb-1.mmlab.edu.gr/
* python3 Producer.py
* python3 Consumer.py
* /ndn/edu/colostate/%40GUEST/fotiou%40aueb.gr
* ndnpingserver /ndn/gr/aueb/fotiou/test