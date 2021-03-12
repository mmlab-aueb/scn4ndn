# SCN4NDN mininet
This folder includes a mininet script that setups a simple topology, which can be used for
validating NDN application

## Prerequisites 
In addition to mininet, make sure you have installed NFD,
[infoedit](https://github.com/NDN-Routing/infoedit) and `python-ndn`

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
