from iprandom import ipv4_address
from iprandom import ipv6_address
from string import hexdigits
from ipaddress import IPv4Address


# private network ip cidr
# 10.0.0.0/8
# 100.64.0.0/10
# 172.16.0.0/12
# 192.0.0.0/24
# 192.168.0.0/16
# 198.18.0.0/15


def test_ipv4_address():
    ip_address = ipv4_address()
    assert ip_address
    assert isinstance(ip_address, str)
    assert 7 <= len(ip_address) <= 15

    split_ip_address = ip_address.split(".")
    assert isinstance(split_ip_address, list)
    assert len(split_ip_address) == 4
    for i in split_ip_address:
        assert i.isdigit()
        assert 0 <= int(i) <= 255

    ip_address = ipv4_address(private_network_allowed=False)
    assert ip_address
    # 10.0.0.0/8
    assert not ip_address.startswith("10.")
    # 100.64.0.0/10
    for i in range(64, 128):
        assert not ip_address.startswith(f"100.{i}")


def test_ipv4_address_10000_times():
    for i in range(10000):
        test_ipv4_address()


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
