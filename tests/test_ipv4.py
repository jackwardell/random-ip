from iprandom.ip_v4 import IPv4AddressRange
from ipaddress import IPv4Address
from ipaddress import AddressValueError


def test_ip_v4_address_range():
    from pytest import raises

    start_ip, end_ip = "0.0.0.0", "255.255.255.255"
    start_ipv4, end_ipv4 = IPv4Address(start_ip), IPv4Address(end_ip)
    ip_address_range = IPv4AddressRange(start_ip, end_ip)
    assert ip_address_range
    assert ip_address_range.start_ip == start_ip
    # assert ip_address_range.start_ip_parts == tuple(int(i) for i in start_ip.split("."))
    assert ip_address_range.end_ip == end_ip
    # assert ip_address_range.end_ip_parts == tuple(int(i) for i in end_ip.split("."))
    assert ip_address_range.ip_range == range(int(start_ipv4), int(end_ipv4) + 1)

    with raises(AddressValueError):
        IPv4AddressRange("asgdjka", "asdkas")

    with raises(AddressValueError):
        IPv4AddressRange("234234.4.324.2", "23423.423.4.2")

    with raises(AddressValueError):
        IPv4AddressRange("0.0.0", "155.6.6")

    start_ip, end_ip = "255.255.255.255", "0.0.0.0"
    with raises(AssertionError):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "10.10.0.0", "10.0.0.0"
    with raises(AssertionError):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "10.10.10.0", "10.10.0.0"
    with raises(AssertionError):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "10.10.10.10", "10.10.10.0"
    with raises(AssertionError):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "0.0.0.0", "0.0.0.0"
    with raises(AssertionError):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    ip_address_range = IPv4AddressRange("0.0.0.0", "255.255.255.255")
    assert "1.2.3.4" in ip_address_range

    ip_address_range = IPv4AddressRange("127.0.0.0", "255.255.255.0")
    assert "1.2.3.4" not in ip_address_range
    assert "127.0.0.0" in ip_address_range
    assert "255.255.255.0" in ip_address_range
    assert "255.255.255.1" not in ip_address_range
