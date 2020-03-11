from iprandom import ipv4_address
from iprandom import ipv6_address

def test_ipv4_address():
    ip_address = ipv4_address()
    assert ip_address
    assert isinstance(ip_address, str)
    assert 7 <= len(ip_address) <= 15

    split_ip_address = ip_address.split(".")
    assert len(split_ip_address) == 4
    assert isinstance(split_ip_address, list)
    for i in split_ip_address:
        assert i.isdigit()
        assert 0 <= int(i) <= 255


# def test_ipv6_address():