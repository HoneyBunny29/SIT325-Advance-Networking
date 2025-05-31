from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class MeshTopo(Topo):
    def build(self, n=10):
        switches = []
        hosts = []

        # Add switches
        for i in range(1, n + 1):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)

        # Add hosts and connect them to switches
        for i in range(1, 21):
            host = self.addHost(f'h{i}')
            hosts.append(host)
            # Connect each host to a switch (round-robin)
            self.addLink(host, switches[(i-1) % n])

        # Connect switches in a full mesh
        for i in range(n):
            for j in range(i + 1, n):
                self.addLink(switches[i], switches[j])

def run():
    topo = MeshTopo()
    net = Mininet(topo=topo, controller=None, link=TCLink)
    
    # Connect to remote ONOS controller
    net.addController('c0', controller=RemoteController, ip='172.17.0.2', port=6653)
    
    net.start()

    # Launch the CLI to run ping manually
    CLI(net)
    
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
