import random
import ipaddress


# special address blocks
# from wikipedia, https://en.wikipedia.org/wiki/Reserved_IP_addresses

# special_address_blocks = {
#     "0.0.0.0/8": ((0, 0, 0, 0), (0, 255, 255, 255)),
#     "10.0.0.0/8": ((10, 0, 0, 0), (10, 255, 255, 255)),
# }


# private network ip cidr
# 10.0.0.0/8      =  10.0.0.0–10.255.255.255
# 100.64.0.0/10   =  100.64.0.0–100.127.255.255
# 172.16.0.0/12   =  172.16.0.0–172.31.255.255
# 192.0.0.0/24    =  192.0.0.0–192.0.0.255
# 192.168.0.0/16  =  192.168.0.0–192.168.255.255
# 198.18.0.0/15   =  198.18.0.0–198.19.255.255

# software ip cidr
# 0.0.0.0/8	= 0.0.0.0–0.255.255.255

# host ip cidr
# 127.0.0.0/8 = 127.0.0.0–127.255.255.255

# subnet ip cidr
# 169.254.0.0/16      =  69.254.0.0–169.254.255.255
# 255.255.255.255/32  =  255.255.255.255

# documentation ip cidr
# 192.0.2.0/24	  =  192.0.2.0–192.0.2.255
# 198.51.100.0/24 =  198.51.100.0–198.51.100.255
# 203.0.113.0/24  =  203.0.113.0–203.0.113.255

# reserved_internet ip cidr
# 192.88.99.0/24  =  192.88.99.0–192.88.99.255
# 224.0.0.0/4     =  224.0.0.0–239.255.255.255
# 240.0.0.0/4	  =  240.0.0.0–255.255.255.254


def ipv4_address(
        private_network_allowed: bool = True,
        software_allowed: bool = True,
        host_allowed: bool = True,
        subnet_allowed: bool = True,
        documentation_allowed: bool = True,
        reserved_internet_allowed: bool = True,
):
    """
    get a random ip address
    """
    # ip_address_parts = [random.randint(0, 255) for _ in range(4)]
    ip_address_parts = [
        random.randint(191, 193),
        88, 99,
        random.randint(0, 255),
    ]

    def _construct_ip_address():
        return ".".join([str(part) for part in ip_address_parts])

    if not private_network_allowed:
        # 10.0.0.0/8 = 10.0.0.0–10.255.255.255
        if ip_address_parts[0] == 10:
            return ipv4_address(private_network_allowed=False)
        # 100.64.0.0/10 = 100.64.0.0–100.127.255.255
        elif ip_address_parts[0] == 100 and 64 <= ip_address_parts[1] <= 127:
            return ipv4_address(private_network_allowed=False)
        # 172.16.0.0/12 = 172.16.0.0–172.31.255.255
        elif ip_address_parts[0] == 172 and 16 <= ip_address_parts[1] <= 31:
            return ipv4_address(private_network_allowed=False)
        # 192.0.0.0/24 = 192.0.0.0–192.0.0.255
        elif ip_address_parts[0:3] == [192, 0, 0]:
            return ipv4_address(private_network_allowed=False)
        # 192.168.0.0/16 = 192.168.0.0–192.168.255.255
        elif ip_address_parts[0:2] == [192, 168]:
            return ipv4_address(private_network_allowed=False)
        # 198.18.0.0/15 = 198.18.0.0–198.19.255.255
        elif ip_address_parts[0:2] in ([198, 18], [198, 19]):
            return ipv4_address(private_network_allowed=False)
        else:
            return _construct_ip_address()

    if not software_allowed:
        # 0.0.0.0/8	= 0.0.0.0–0.255.255.255
        if ip_address_parts[0] == 0:
            return ipv4_address(software_allowed=False)
        else:
            return _construct_ip_address()

    if not host_allowed:
        # 127.0.0.0/8 = 127.0.0.0–127.255.255.255
        if ip_address_parts[0] == 127:
            return ipv4_address(host_allowed=False)
        else:
            return _construct_ip_address()

    if not subnet_allowed:
        # 169.254.0.0/16 = 169.254.0.0–169.254.255.255
        if ip_address_parts[0:2] == [169, 254]:
            return ipv4_address(subnet_allowed=False)
        # 255.255.255.255/32 = 255.255.255.255
        elif ip_address_parts == [255, 255, 255, 255]:
            return ipv4_address(subnet_allowed=False)
        else:
            return _construct_ip_address()

    if not documentation_allowed:
        # 192.0.2.0/24 = 192.0.2.0–192.0.2.255
        if ip_address_parts[0:3] == [192, 0, 2]:
            return ipv4_address(documentation_allowed=False)
        # 198.51.100.0/24 = 198.51.100.0–198.51.100.255
        if ip_address_parts[0:3] == [198, 51, 100]:
            return ipv4_address(documentation_allowed=False)
        # 203.0.113.0/24 = 203.0.113.0–203.0.113.255
        if ip_address_parts[0:3] == [203, 0, 113]:
            return ipv4_address(documentation_allowed=False)
        else:
            return _construct_ip_address()

    if not reserved_internet_allowed:
        # 192.88.99.0/24  =  192.88.99.0–192.88.99.255
        if ip_address_parts[0:3] == [192, 88, 99]:
            return ipv4_address(reserved_internet_allowed=False)
        else:
            return _construct_ip_address()

    else:
        return _construct_ip_address()


def ipv6_address():
    return ":".join("{:04x}".format(random.randint(0, 65535)) for _ in range(8))
