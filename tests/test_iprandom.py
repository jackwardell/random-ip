from ipaddress import IPv4Address
from random import choice

from pytest import raises

from iprandom import IPv4AddressRange, AddressValueError
# from iprandom import IPv4Generator
from iprandom import _Ranges
from ipaddress import IPv4Network


def test_ip_v4_address_range():
    start_ip, end_ip = "0.0.0.0", "255.255.255.255"
    start_ipv4, end_ipv4 = IPv4Address(start_ip), IPv4Address(end_ip)
    ip_address_range = IPv4AddressRange(start_ip, end_ip)
    assert ip_address_range
    assert ip_address_range.start_ip == start_ip
    assert ip_address_range.end_ip == end_ip
    assert ip_address_range.int_ip_range == range(int(start_ipv4), int(end_ipv4) + 1)

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

    ip_address_range = IPv4AddressRange("127.0.0.0", "255.255.255.0")
    assert ip_address_range != range(2130706432, 4294967040)
    assert ip_address_range == IPv4AddressRange("127.0.0.0", "255.255.255.0")

    # assert repr(ip_address_range) == (
    #     "IPv4AddressRange(start_ip_address=127.0.0.0, end_ip_address=255.255.255.0)"
    # )
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
        chain_range = _Ranges()

    chain_range = _Ranges(range1)
    assert chain_range._boundaries_and_ranges == {10: range1}

    assert len(chain_range) == len(range1)
    assert chain_range[0] == 0
    assert chain_range[0] == range1[0]
    assert chain_range[5] == 5
    assert chain_range[5] == range1[5]
    assert chain_range[9] == 9
    assert chain_range[9] == range1[9]
    assert chain_range[-1] == range1[-1]

    chain_range = _Ranges(range1, range2)
    assert chain_range._boundaries_and_ranges == {10: range1, 60: range2}

    assert len(chain_range) == len(range1) + len(range2)
    assert chain_range[0] == 0
    assert chain_range[0] == range1[0]
    assert chain_range[5] == 5
    assert chain_range[5] == range1[5]
    assert chain_range[9] == 9
    assert chain_range[9] == range1[9]
    assert chain_range[10] == 50
    assert chain_range[-50] == 50
    assert chain_range[-51] == 9
    assert chain_range[10] == range2[(10 - len(range1))]
    assert chain_range[20] == 60
    assert chain_range[20] == range2[(20 - len(range1))]
    assert chain_range[59] == 99
    assert chain_range[59] == range2[(59 - len(range1))]
    assert chain_range[-1] == 99

    with raises(IndexError):
        chain_range[len(chain_range)]

    assert chain_range[len(chain_range) - 1] == 99

    # change order
    chain_range = _Ranges(range2, range1)
    assert chain_range._boundaries_and_ranges == {50: range2, 60: range1}
    # assert chain_range.ranges == (range2, range1)

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

    chain_range = _Ranges(range1, range1)
    assert chain_range._boundaries_and_ranges == {10: range1, 20: range1}
    # assert chain_range.ranges == (range1, range1)

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

    chain_range = _Ranges(range1, range2, range3)
    assert len(chain_range) == len(range1) + len(range2) + len(range3)
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
    assert chain_range[60] == 1000
    assert chain_range[1059] == 1999
    assert chain_range[-1] == 1999

    assert choice(chain_range)

    iterable = [range1, range2, range3]
    chain_range = _Ranges.from_iterable(iterable)
    assert chain_range
    assert len(chain_range) == len(range1) + len(range2) + len(range3)
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
    assert chain_range[60] == 1000
    assert chain_range[1059] == 1999
    assert chain_range[-1] == 1999

    assert choice(chain_range)


# def test_ip_generator():
#     random_ip_generator = IPv4Generator()
#     random_ip = random_ip_generator()
#     assert random_ip
#     assert isinstance(random_ip, str)
#
#     random_ip_generator = IPv4Generator(
#         included_ranges=[IPv4AddressRange("0.0.0.0", "0.0.0.4")]
#     )
#     random_ip = random_ip_generator()
#     assert random_ip in ("0.0.0.0", "0.0.0.1", "0.0.0.2", "0.0.0.3", "0.0.0.4")
#
#     random_ip_generator = IPv4Generator(included_ranges=[IPv4Network("10.0.0.0/8")])
#     random_ip_address = random_ip_generator()
#     assert random_ip_address.startswith("10.")
#
#     random_ip_generator = IPv4Generator(included_ranges=[IPv4Network("100.64.0.0/10")])
#     random_ip_address = random_ip_generator()
#     assert IPv4Address(random_ip_address) in IPv4Network("100.64.0.0/10")
#     assert (
#         random_ip_address.startswith("100.64.")
#         or random_ip_address.startswith("100.65.")
#         or random_ip_address.startswith("100.66.")
#         or random_ip_address.startswith("100.67.")
#         or random_ip_address.startswith("100.68.")
#         or random_ip_address.startswith("100.69.")
#         or random_ip_address.startswith("100.70.")
#         or random_ip_address.startswith("100.71.")
#         or random_ip_address.startswith("100.72.")
#         or random_ip_address.startswith("100.73.")
#         or random_ip_address.startswith("100.74.")
#         or random_ip_address.startswith("100.75.")
#         or random_ip_address.startswith("100.76.")
#         or random_ip_address.startswith("100.77.")
#         or random_ip_address.startswith("100.78.")
#         or random_ip_address.startswith("100.79.")
#         or random_ip_address.startswith("100.80.")
#         or random_ip_address.startswith("100.81.")
#         or random_ip_address.startswith("100.82.")
#         or random_ip_address.startswith("100.83.")
#         or random_ip_address.startswith("100.84.")
#         or random_ip_address.startswith("100.85.")
#         or random_ip_address.startswith("100.86.")
#         or random_ip_address.startswith("100.87.")
#         or random_ip_address.startswith("100.88.")
#         or random_ip_address.startswith("100.89.")
#         or random_ip_address.startswith("100.90.")
#         or random_ip_address.startswith("100.91.")
#         or random_ip_address.startswith("100.92.")
#         or random_ip_address.startswith("100.93.")
#         or random_ip_address.startswith("100.94.")
#         or random_ip_address.startswith("100.95.")
#         or random_ip_address.startswith("100.96.")
#         or random_ip_address.startswith("100.97.")
#         or random_ip_address.startswith("100.98.")
#         or random_ip_address.startswith("100.99.")
#         or random_ip_address.startswith("100.100.")
#         or random_ip_address.startswith("100.101.")
#         or random_ip_address.startswith("100.102.")
#         or random_ip_address.startswith("100.103.")
#         or random_ip_address.startswith("100.104.")
#         or random_ip_address.startswith("100.105.")
#         or random_ip_address.startswith("100.106.")
#         or random_ip_address.startswith("100.107.")
#         or random_ip_address.startswith("100.108.")
#         or random_ip_address.startswith("100.109.")
#         or random_ip_address.startswith("100.110.")
#         or random_ip_address.startswith("100.111.")
#         or random_ip_address.startswith("100.112.")
#         or random_ip_address.startswith("100.113.")
#         or random_ip_address.startswith("100.114.")
#         or random_ip_address.startswith("100.115.")
#         or random_ip_address.startswith("100.116.")
#         or random_ip_address.startswith("100.117.")
#         or random_ip_address.startswith("100.118.")
#         or random_ip_address.startswith("100.119.")
#         or random_ip_address.startswith("100.120.")
#         or random_ip_address.startswith("100.121.")
#         or random_ip_address.startswith("100.122.")
#         or random_ip_address.startswith("100.123.")
#         or random_ip_address.startswith("100.124.")
#         or random_ip_address.startswith("100.125.")
#         or random_ip_address.startswith("100.126.")
#         or random_ip_address.startswith("100.127.")
#     )
#
#     random_ip_generator = IPv4Generator(included_ranges=[IPv4Network("172.16.0.0/12")])
#     random_ip_address = random_ip_generator()
#     assert IPv4Address(random_ip_address) in IPv4Network("172.16.0.0/12")
#     assert (
#         random_ip_address.startswith("172.16.")
#         or random_ip_address.startswith("172.17.")
#         or random_ip_address.startswith("172.18.")
#         or random_ip_address.startswith("172.19.")
#         or random_ip_address.startswith("172.20.")
#         or random_ip_address.startswith("172.21.")
#         or random_ip_address.startswith("172.22.")
#         or random_ip_address.startswith("172.23.")
#         or random_ip_address.startswith("172.24.")
#         or random_ip_address.startswith("172.25.")
#         or random_ip_address.startswith("172.26.")
#         or random_ip_address.startswith("172.27.")
#         or random_ip_address.startswith("172.28.")
#         or random_ip_address.startswith("172.29.")
#         or random_ip_address.startswith("172.30.")
#         or random_ip_address.startswith("172.31.")
#     )
#
#     random_ip_generator = IPv4Generator(included_ranges=[IPv4Network("192.0.0.0/24")])
#     random_ip_address = random_ip_generator()
#     assert IPv4Address(random_ip_address) in IPv4Network("192.0.0.0/24")
#     assert random_ip_address.startswith("192.0.0.")
#
#     random_ip_generator = IPv4Generator(included_ranges=[IPv4Network("192.168.0.0/16")])
#     random_ip_address = random_ip_generator()
#     assert IPv4Address(random_ip_address) in IPv4Network("192.168.0.0/16")
#     assert random_ip_address.startswith("192.168.")
#
#     random_ip_generator = IPv4Generator(included_ranges=[IPv4Network("198.18.0.0/15")])
#     random_ip_address = random_ip_generator()
#     assert IPv4Address(random_ip_address) in IPv4Network("198.18.0.0/15")
#     assert random_ip_address.startswith("198.18") or random_ip_address.startswith(
#         "198.19."
#     )
