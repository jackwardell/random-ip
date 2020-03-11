import random
import ipaddress


# reserved ips


def ipv4_address():
    return ".".join([str(random.randint(0, 255)) for _ in range(4)])


def ipv6_address():
    return ':'.join('{:04x}'.format(random.randint(0, 65535)) for _ in range(8))
