# SCN4NDN mininet
This folder includes a mininet script that setups a simple topology, which can be used for
validating NDN application


## Prerequisites 
* Install NFD from [sources](https://github.com/named-data/NFD)
* Install mininet with python3 support (`sudo PYTHON=python3 mininet/util/install.sh -n`) 
* Install [infoedit](https://github.com/NDN-Routing/infoedit) 
* Install `python-ndn` as global module (`sudo -H pip3 install python-ndn`)

## Execution
Run `sudo python3 simple_topology.py` In the `mininet>` command prompt run `xterm consumer, producer`. In the xterm 
of `producer` run

```
export HOME=/tmp/mininet/producer
python3 Producer.py
```

In the xterm 
of `consumer` run

```
export HOME=/tmp/mininet/consumer
python3 Consumer.py
```
