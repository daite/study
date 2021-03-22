import ipaddress 
import socket
import struct
import sys
import os

HOST = 'HOST'

class IP:
    def __init__(self, buff):
        headers = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = headers[0] >> 4
        self.ihl = headers[0] & 0xF
        self.tos = headers[1]
        self.len = headers[2]
        self.id = headers[3]
        self.offset = headers[4]
        self.ttl = headers[5]
        self.protocol_num = headers[6]
        self.sum = headers[7]
        self.src = headers[8]
        self.dst = headers[9]
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print("%s No protocol for %s" %(e, self.protocol_num))
            self.protocol = str(self.protocol_num)

class ICMP:
    def __init__(self, buff):
        headers = struct.unpack("<BBHHH", buff)
        self.type = headers[0]
        self.code = headers[1]
        self.sum = headers[2]
        self.id = headers[3]
        self.seq = headers[4]


def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ip_header = IP(raw_buffer[0:20])
            if ip_header.protocol == "ICMP":
                # ip_header_size = 20 bytes
                print("Protocol: %s %s -> %s" %(ip_header.protocol,
                ip_header.src_address, ip_header.dst_address))
                print(f'Version: {ip_header.ver}')
                print(f'Header Lenght: {ip_header.ihl} TTL: {ip_header.ttl}')
                offset = ip_header.ihl * 4
                buf = raw_buffer[offset:offset + 8]
                icmp_header = ICMP(buf)
                print("ICMP -> Type: %s Code: %s\n" %(
                    icmp_header.type, icmp_header.code))

            else:
                print("Protocol: %s %s -> %s" %(ip_header.protocol,
                    ip_header.src_address, ip_header.dst_address))
    except KeyboardInterrupt:
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()

if __name__ == '__main__':
    sniff(HOST)
