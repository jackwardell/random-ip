import random
import ipaddress

# special address blocks
# from wikipedia, https://en.wikipedia.org/wiki/Reserved_IP_addresses

special_address_blocks = {
    "0.0.0.0/8": ((0, 0, 0, 0), (0, 255, 255, 255)),
    "10.0.0.0/8": ((10, 0, 0, 0), (10, 255, 255, 255))
}

# private network ip cidr
# 10.0.0.0/8
# 100.64.0.0/10
# 172.16.0.0/12
# 192.0.0.0/24
# 192.168.0.0/16
# 198.18.0.0/15


def ipv4_address(private_network_allowed: bool = True):
    """
    get a random ip address
    """
    ip_address_parts = [random.randint(0, 255) for _ in range(4)]

    if private_network_allowed:
        return ".".join([str(part) for part in ip_address_parts])

    elif not private_network_allowed:
        # 10.0.0.0/8
        if ip_address_parts[0] == 10:
            return ipv4_address(private_network_allowed=False)

        # 100.64.0.0/10
        elif ip_address_parts[0] == 100 and 64 <= ip_address_parts[1] <= 127:
            return ipv4_address(private_network_allowed=False)

        else:
            return ".".join([str(part) for part in ip_address_parts])





def ipv6_address():
    return ":".join("{:04x}".format(random.randint(0, 65535)) for _ in range(8))
