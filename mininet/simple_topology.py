#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import Topo
from mininet.net import Mininet
import time
import subprocess
from mininet.nodelib import NAT

class SingleSwitchTopo(Topo):
    def build(self):
        hosts  = [ self.addHost( h ) for h in ['h1', 'h2'] ]
        s1 = self.addSwitch( 's1' )
        for h in hosts:
            self.addLink( s1, h )

def start_nfd(node):
    homeDir = '/tmp/mininet/{}'.format(node.name)
    node.cmd('rm -rf {}'.format(homeDir)) # fresh start
    node.cmd('mkdir -p {}'.format(homeDir))
    node.cmd('export HOME={} && cd ~'.format(homeDir))
    ndnFolder  = '{}/.ndn'.format(homeDir)
    node.cmd('mkdir -p {}'.format(ndnFolder))
    confFile   = '{}/nfd.conf'.format(homeDir)
    logFile    = 'nfd.log'
    sockFile   = '/run/{}.sock'.format(node.name)
    clientConf = '{}/client.conf'.format(ndnFolder)
    node.cmd('cp /usr/local/etc/ndn/nfd.conf.sample {}'.format(confFile))
    node.cmd('cp /usr/local/etc/ndn/client.conf.sample {}'.format(clientConf))
    # Open the conf file and change socket file name
    node.cmd('infoedit -f {} -s face_system.unix.path -v {}'.format(confFile, sockFile))
   
    # Change the unix socket
    node.cmd('sudo sed -i "s|;transport|transport|g" {}'.format(clientConf))
    node.cmd('sudo sed -i "s|nfd.sock|{}.sock|g" {}'.format(node.name, clientConf))
    node.cmd('ndnsec-keygen /scn4ndn | ndnsec-install-cert -')
    print("Starting with config file {}".format(confFile))
    node.cmd('nfd --config {} > /dev/null  2>&1&'.format(confFile))



if __name__ == '__main__':
    lg.setLogLevel( 'info')
    topo = SingleSwitchTopo()
    net = Mininet(topo)
    net.start()
    time.sleep(2)
    info( "*** Hosts are running and should have internet connectivity\n" )
    info( "*** Type 'exit' or control-D to shut down network\n" )
    node = net.hosts[0]
    start_nfd(node)
    time.sleep(2)
    node = net.hosts[1]
    start_nfd(node)
    time.sleep(2)
    CLI( net )
    # Shut down NAT
    subprocess.run(["nfd-stop"])
    net.stop()
