from iprandom import ipv4_address
from iprandom import ipv6_address
from string import hexdigits


def test_ipv4_address():
    ip_address = ipv4_address()
    assert ip_address
    assert isinstance(ip_address, str)
    assert 7 <= len(ip_address) <= 15

    _split_ip_address = ip_address.split(".")
    assert isinstance(_split_ip_address, list)
    assert len(_split_ip_address) == 4
    for i in _split_ip_address:
        assert i.isdigit()
        assert 0 <= int(i) <= 255


def test_ipv4_address_private_network_not_allowed():
    """
    private network ip cidr
    10.0.0.0/8      =  10.0.0.0–10.255.255.255
    100.64.0.0/10   =  100.64.0.0–100.127.255.255
    172.16.0.0/12   =  172.16.0.0–172.31.255.255
    192.0.0.0/24    =  192.0.0.0–192.0.0.255
    192.168.0.0/16  =  192.168.0.0–192.168.255.255
    198.18.0.0/15   =  198.18.0.0–198.19.255.255
    """
    ip_address = ipv4_address(private_network_allowed=False)
    assert ip_address
    # 10.0.0.0/8
    assert not ip_address.startswith("10.")
    # 100.64.0.0/10
    assert not ip_address.startswith("100.64.")
    assert not ip_address.startswith("100.65.")
    assert not ip_address.startswith("100.66.")
    assert not ip_address.startswith("100.67.")
    assert not ip_address.startswith("100.68.")
    assert not ip_address.startswith("100.69.")
    assert not ip_address.startswith("100.70.")
    assert not ip_address.startswith("100.71.")
    assert not ip_address.startswith("100.72.")
    assert not ip_address.startswith("100.73.")
    assert not ip_address.startswith("100.74.")
    assert not ip_address.startswith("100.75.")
    assert not ip_address.startswith("100.76.")
    assert not ip_address.startswith("100.77.")
    assert not ip_address.startswith("100.78.")
    assert not ip_address.startswith("100.79.")
    assert not ip_address.startswith("100.80.")
    assert not ip_address.startswith("100.81.")
    assert not ip_address.startswith("100.82.")
    assert not ip_address.startswith("100.83.")
    assert not ip_address.startswith("100.84.")
    assert not ip_address.startswith("100.85.")
    assert not ip_address.startswith("100.86.")
    assert not ip_address.startswith("100.87.")
    assert not ip_address.startswith("100.88.")
    assert not ip_address.startswith("100.89.")
    assert not ip_address.startswith("100.90.")
    assert not ip_address.startswith("100.91.")
    assert not ip_address.startswith("100.92.")
    assert not ip_address.startswith("100.93.")
    assert not ip_address.startswith("100.94.")
    assert not ip_address.startswith("100.95.")
    assert not ip_address.startswith("100.96.")
    assert not ip_address.startswith("100.97.")
    assert not ip_address.startswith("100.98.")
    assert not ip_address.startswith("100.99.")
    assert not ip_address.startswith("100.100.")
    assert not ip_address.startswith("100.101.")
    assert not ip_address.startswith("100.102.")
    assert not ip_address.startswith("100.103.")
    assert not ip_address.startswith("100.104.")
    assert not ip_address.startswith("100.105.")
    assert not ip_address.startswith("100.106.")
    assert not ip_address.startswith("100.107.")
    assert not ip_address.startswith("100.108.")
    assert not ip_address.startswith("100.109.")
    assert not ip_address.startswith("100.110.")
    assert not ip_address.startswith("100.111.")
    assert not ip_address.startswith("100.112.")
    assert not ip_address.startswith("100.113.")
    assert not ip_address.startswith("100.114.")
    assert not ip_address.startswith("100.115.")
    assert not ip_address.startswith("100.116.")
    assert not ip_address.startswith("100.117.")
    assert not ip_address.startswith("100.118.")
    assert not ip_address.startswith("100.119.")
    assert not ip_address.startswith("100.120.")
    assert not ip_address.startswith("100.121.")
    assert not ip_address.startswith("100.122.")
    assert not ip_address.startswith("100.123.")
    assert not ip_address.startswith("100.124.")
    assert not ip_address.startswith("100.125.")
    assert not ip_address.startswith("100.126.")
    assert not ip_address.startswith("100.127.")
    # 172.16.0.0/12
    assert not ip_address.startswith("172.16.")
    assert not ip_address.startswith("172.17.")
    assert not ip_address.startswith("172.18.")
    assert not ip_address.startswith("172.19.")
    assert not ip_address.startswith("172.20.")
    assert not ip_address.startswith("172.21.")
    assert not ip_address.startswith("172.22.")
    assert not ip_address.startswith("172.23.")
    assert not ip_address.startswith("172.24.")
    assert not ip_address.startswith("172.25.")
    assert not ip_address.startswith("172.26.")
    assert not ip_address.startswith("172.27.")
    assert not ip_address.startswith("172.28.")
    assert not ip_address.startswith("172.29.")
    assert not ip_address.startswith("172.30.")
    assert not ip_address.startswith("172.31.")
    # 192.0.0.0/24
    assert not ip_address.startswith("192.0.0.")
    # 192.168.0.0/16
    assert not ip_address.startswith("192.168.")
    # 198.18.0.0/15
    assert not ip_address.startswith("198.18.")
    assert not ip_address.startswith("198.19.")


def test_ipv4_address_software_not_allowed():
    """
    software ip cidr
    0.0.0.0/8 = 0.0.0.0–0.255.255.255
    """
    ip_address = ipv4_address(software_allowed=False)
    assert ip_address
    assert not ip_address.startswith("0.")


def test_ipv4_address_host_not_allowed():
    """
    host ip cidr
    127.0.0.0/8 = 127.0.0.0–127.255.255.255
    """
    ip_address = ipv4_address(host_allowed=False)
    assert ip_address
    assert not ip_address.startswith("127.")


def test_ipv4_address_subnet_not_allowed():
    """
    subnet ip cidr
    169.254.0.0/16      =  169.254.0.0–169.254.255.255
    255.255.255.255/32  =  255.255.255.255
    """
    ip_address = ipv4_address(subnet_allowed=False)
    assert ip_address
    # 169.254.0.0/16
    assert not ip_address.startswith("169.254.")
    # 255.255.255.255/32
    assert not ip_address == "255.255.255.255"


def test_ipv4_address_documentation_not_allowed():
    """
    192.0.2.0/24     =  192.0.2.0–192.0.2.255
    198.51.100.0/24  =  198.51.100.0–198.51.100.255
    203.0.113.0/24   =  203.0.113.0–203.0.113.255
    """
    ip_address = ipv4_address(documentation_allowed=False)
    assert ip_address
    # 192.0.2.0/24
    assert not ip_address.startswith("192.0.2.")
    # 198.51.100.0/24
    assert not ip_address.startswith("198.51.100.")
    # 203.0.113.0/24
    assert not ip_address.startswith("203.0.113.")


def test_ipv4_address_reserved_internet_not_allowed():
    """
    192.88.99.0/24  =  192.88.99.0–192.88.99.255
    224.0.0.0/4     =  224.0.0.0–239.255.255.255
    240.0.0.0/4	  =  240.0.0.0–255.255.255.254
    """
    ip_address = ipv4_address(reserved_internet_allowed=False)
    assert ip_address
    # 192.88.99.0/24
    assert not ip_address.startswith("192.88.99.")


def test_ipv4_address_100000_times():
    for i in range(1000000):
        test_ipv4_address()
        test_ipv4_address_private_network_not_allowed()
        test_ipv4_address_software_not_allowed()
        test_ipv4_address_host_not_allowed()
        test_ipv4_address_subnet_not_allowed()
        test_ipv4_address_documentation_not_allowed()
        test_ipv4_address_reserved_internet_not_allowed()


def test_ipv6_address():
    ip_address = ipv6_address()
    assert ip_address
    assert isinstance(ip_address, str)
    assert len(ip_address) == 39

    split_ip_address = ip_address.split(":")
    assert isinstance(split_ip_address, list)
    assert len(split_ip_address) == 8
    for i in split_ip_address:
        assert str(int(i, 16)).isdigit()
        assert all([j in hexdigits for j in i])
        assert 0 < int(i, 16) < int("ffff", 16)
