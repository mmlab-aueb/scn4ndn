#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import Topo
from mininet.net import Mininet
import time

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch)

def start_nfd(node):
    homeDir = '/tmp/mininet/{}'.format(node.name)
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
    node.cmd('ndnsec-keygen /localhost/operator | ndnsec-install-cert -')
    print("Starting with config file {}".format(confFile))
    node.cmd('nfd --config {} > /dev/null  2>&1&'.format(confFile))



if __name__ == '__main__':
    lg.setLogLevel( 'info')
    topo = SingleSwitchTopo(n=2)
    net = Mininet(topo)
    net.start()
    time.sleep(2)
    info( "*** Hosts are running and should have internet connectivity\n" )
    info( "*** Type 'exit' or control-D to shut down network\n" )
    node = net.hosts[0]
    node.setIP("10.0.0.5")
    start_nfd(node)
    time.sleep(2)
    node = net.hosts[1]
    node.setIP("10.0.0.6")
    start_nfd(node)
    time.sleep(2)
    CLI( net )
    # Shut down NAT
    net.stop()
