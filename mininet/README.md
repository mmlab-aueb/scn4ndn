## Prerequisites

* sudo -H pip3  install python-ndn

Infoedit
```
git clone --depth 1 https://github.com/NDN-Routing/infoedit
cd infoedit
make
sudo make install
```

## Useful nfdc commands
* export HOME=/tmp/mininet/h1
* nfd --config /tmp/mininet/h1/nfd.conf
* nfdc face create udp://10.0.0.6
* nfdc route add /example udp://10.0.0.6
* ndnsec-keygen /gr/fotiou/testApp | ndnsec-install-cert -

## Links
* Testbed status http://ndndemo.arl.wustl.edu/
* CSU http://ndn.netsec.colostate.edu/ 
** nfdc face create udp://129.82.138.48 
** nfdc route add /ndn udp://129.82.138.48
** nfdc route add /localhop/nfd udp://129.82.138.48