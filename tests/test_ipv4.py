from iprandom.ip_v4 import IPv4AddressRange
from ipaddress import IPv4Address
from ipaddress import AddressValueError
from pytest import raises
from iprandom.ip_v4 import ChainRange
from itertools import chain


def test_ip_v4_address_range():
    start_ip, end_ip = "0.0.0.0", "255.255.255.255"
    start_ipv4, end_ipv4 = IPv4Address(start_ip), IPv4Address(end_ip)
    ip_address_range = IPv4AddressRange(start_ip, end_ip)
    assert ip_address_range
    assert ip_address_range.start_ip == start_ip
    assert ip_address_range.end_ip == end_ip
    assert ip_address_range.ip_range == range(int(start_ipv4), int(end_ipv4) + 1)

    with raises(ValueError):
        IPv4AddressRange("asgdjka", "asdkas")

    with raises(ValueError):
        IPv4AddressRange("234234.4.324.2", "23423.423.4.2")

    with raises(ValueError):
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

    ip_address_range = IPv4AddressRange("127.0.0.0", "255.255.255.0")
    assert ip_address_range != range(2130706432, 4294967040)
    assert ip_address_range == IPv4AddressRange("127.0.0.0", "255.255.255.0")

    assert repr(ip_address_range) == (
        "IPv4AddressRange(start_ip_address=127.0.0.0, end_ip_address=255.255.255.0)"
    )
    assert str(ip_address_range) == "127.0.0.0 - 255.255.255.0"

    ip_address_range = IPv4AddressRange("0.0.0.0", "0.0.0.4")
    assert ip_address_range.count("0.0.0.0") == 1
    assert ip_address_range.count("0.0.0.1") == 1
    assert ip_address_range.count("0.0.0.2") == 1
    assert ip_address_range.count("0.0.0.3") == 1
    assert ip_address_range.count("0.0.0.4") == 1
    assert ip_address_range.count("0.0.0.5") == 0

    assert ip_address_range.index("0.0.0.0") == 0
    assert ip_address_range.index("0.0.0.1") == 1
    assert ip_address_range.index("0.0.0.2") == 2
    assert ip_address_range.index("0.0.0.3") == 3
    assert ip_address_range.index("0.0.0.4") == 4
    with raises(ValueError):
        ip_address_range.index("0.0.0.5")

    assert ip_address_range.to_cidr() == ["0.0.0.0/30", "0.0.0.4/32"]

    ip_address_range = IPv4AddressRange("0.0.0.0", "255.255.255.255")
    assert ip_address_range.to_cidr() == ["0.0.0.0/0"]

    start_ip, end_ip = IPv4Address("0.0.0.0"), IPv4Address("255.255.255.255")
    ip_address_range = IPv4AddressRange(start_ip, end_ip)

    assert ip_address_range.start_ip == start_ip.exploded
    assert ip_address_range.end_ip == end_ip.exploded
    assert ip_address_range._start_ip == start_ip
    assert ip_address_range._end_ip == end_ip


def test_chain_range():
    range1, range2, range3 = range(0, 10), range(50, 100), range(1000, 2000)
    with raises(TypeError):
        chain_range = ChainRange()

    chain_range = ChainRange(range1, range2)
    assert chain_range.boundaries_and_ranges == {10: range1, 60: range2}
    assert chain_range.ranges == (range1, range2)

    assert len(chain_range) == len(range1) + len(range2)
    assert chain_range[0] == 0
    assert chain_range[0] == range1[0]
    assert chain_range[5] == 5
    assert chain_range[5] == range1[5]
    assert chain_range[9] == 9
    assert chain_range[9] == range1[9]
    assert chain_range[10] == 50
    assert chain_range[10] == range2[(10 - len(range1))]
    assert chain_range[20] == 60
    assert chain_range[20] == range2[(20 - len(range1))]
    assert chain_range[59] == 99
    assert chain_range[59] == range2[(59 - len(range1))]

    with raises(IndexError):
        chain_range[len(chain_range)]

    assert chain_range[len(chain_range) - 1] == 99

    # change order
    chain_range = ChainRange(range2, range1)
    assert chain_range.boundaries_and_ranges == {50: range2, 60: range1}
    assert chain_range.ranges == (range2, range1)

    assert len(chain_range) == len(range2) + len(range1)
    assert chain_range[0] == 50
    assert chain_range[0] == range2[0]
    assert chain_range[5] == 55
    assert chain_range[5] == range2[5]
    assert chain_range[9] == 59
    assert chain_range[9] == range2[9]
    assert chain_range[10] == 60
    assert chain_range[20] == 70
    assert chain_range[59] == 9
    assert chain_range[59] == range1[(59 - len(range2))]

    with raises(IndexError):
        chain_range[len(chain_range)]

    assert chain_range[len(chain_range) - 1] == 9

    # assert list(chain_range) == list(range2) + list(range1)

    for i in range1:
        assert i in chain_range
    for i in range2:
        assert i in chain_range
    for i in range(10, 50):
        assert i not in chain_range

    chain_range = ChainRange(range1, range1)
    assert chain_range.boundaries_and_ranges == {10: range1, 20: range1}
    assert chain_range.ranges == (range1, range1)

    assert len(chain_range) == len(range1) + len(range1)
    assert chain_range[0] == 0
    assert chain_range[0] == range1[0]
    assert chain_range[5] == 5
    assert chain_range[5] == range1[5]
    assert chain_range[9] == 9
    assert chain_range[9] == range1[9]
    assert chain_range[10] == 0
    assert chain_range[15] == 5
    assert chain_range[19] == 9

    with raises(IndexError):
        chain_range[len(chain_range)]

    assert chain_range[len(chain_range) - 1] == 9
