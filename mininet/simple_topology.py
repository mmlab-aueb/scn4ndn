#!/usr/bin/python

from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topo import Topo
from mininet.net import Mininet
import time
import subprocess
from mininet.nodelib import NAT

class SingleSwitchTopo(Topo):
    ''' 
                           forwarder(10.0.0.2)
                               |
                               |  
    producer(10.0.0.1)<---->(switch)<---->consumer(10.0.0.3)
    '''
    def build(self):
        hosts ={
            'producer' :'10.0.0.1/8',
            'forwarder':'10.0.0.2/8',
            'consumer' :'10.0.0.3/8'
        }
        s1 = self.addSwitch( 's1' )
        for host,ip in hosts.items():
            h = self.addHost(host, ip=ip)
            print("Added host", host)
            self.addLink( s1, h )

    def configure_faces(self, net):
        '''
        producer(10.0.0.1)<---->forwarder(10.0.0.3)<---->consumer(10.0.0.2)
        '''
        forwarder = net.hosts[1]
        forwarder.cmd('export HOME=/tmp/mininet/forwarder')
        forwarder.cmd('nfdc face create udp://10.0.0.1')
        forwarder.cmd('nfdc route add /scn4ndn/testApp udp://10.0.0.1')
        consumer = net.hosts[2]
        consumer.cmd('export HOME=/tmp/mininet/consumer')
        consumer.cmd('nfdc face create udp://10.0.0.2')
        consumer.cmd('nfdc route add /scn4ndn/testApp udp://10.0.0.2')
        print("Faces configured")



def start_nfd(net):
    for node in net.hosts:
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
        print("nfd is starting in {}  with config file {}".format(node.name, confFile))
        node.cmd('nfd --config {} > {}/nfd.out  2>&1&'.format(confFile, homeDir))


if __name__ == '__main__':
    lg.setLogLevel( 'info')
    topo = SingleSwitchTopo()
    net = Mininet(topo)
    net.start()
    time.sleep(2)
    start_nfd(net)
    time.sleep(2)
    topo.configure_faces(net)
    print
    info( "*** Hosts are running and should have internet connectivity\n" )
    info( "*** Type 'exit' or control-D to shut down network\n" )
    CLI( net )
    # Shut down NAT
    subprocess.run(["nfd-stop"])
    net.stop()
