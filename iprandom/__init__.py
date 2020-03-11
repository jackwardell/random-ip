import random
import ipaddress

# special address blocks
# from wikipedia, https://en.wikipedia.org/wiki/Reserved_IP_addresses

special_address_blocks = {
    "0.0.0.0/8": ((0, 0, 0, 0), (0, 255, 255, 255)),
    "10.0.0.0/8": ((10, 0, 0, 0), (10, 255, 255, 255)),
}


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


def ipv4_address(
        private_network_allowed: bool = True,
        software_allowed: bool = True,
        host_allowed: bool = True,
):
    """
    get a random ip address
    """
    ip_address_parts = [random.randint(0, 255) for _ in range(4)]

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
        elif ip_address_parts[0] == 192 and ip_address_parts[1:3] == [0, 0]:
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

    else:
        return _construct_ip_address()


def ipv6_address():
    return ":".join("{:04x}".format(random.randint(0, 65535)) for _ in range(8))
