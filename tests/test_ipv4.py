from iprandom.ip_v4 import IPv4AddressRange


def test_ip_v4_address_range():
    from pytest import raises

    start_ip, end_ip = "0.0.0.0", "255.255.255.255"
    ip_address_range = IPv4AddressRange(start_ip, end_ip)
    assert ip_address_range
    assert ip_address_range.start_ip == start_ip
    assert ip_address_range.start_ip_parts == tuple(int(i) for i in start_ip.split("."))
    assert ip_address_range.end_ip == end_ip
    assert ip_address_range.end_ip_parts == tuple(int(i) for i in end_ip.split("."))
    assert ip_address_range.ip_a_range == range(
        int(start_ip.split(".")[0]), int(end_ip.split(".")[0]) + 1
    )

    start_ip, end_ip = "255.255.255.255", "0.0.0.0"
    with raises(
        AssertionError, match="end ip must be greater than or equal to the start ip"
    ):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "10.10.0.0", "10.0.0.0"
    with raises(
        AssertionError, match="end ip must be greater than or equal to the start ip"
    ):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "10.10.10.0", "10.10.0.0"
    with raises(
        AssertionError, match="end ip must be greater than or equal to the start ip"
    ):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "10.10.10.10", "10.10.10.0"
    with raises(
        AssertionError, match="end ip must be greater than or equal to the start ip"
    ):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)

    start_ip, end_ip = "0.0.0.0", "0.0.0.0"
    with raises(
        AssertionError, match="start and end ips match - ip ranges should not match"
    ):
        ip_address_range = IPv4AddressRange(start_ip, end_ip)
