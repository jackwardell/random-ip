def check_is_ipv4_address(ip_address):
    assert isinstance(ip_address, str), "ip address must be a string"
    assert (
        7 <= len(ip_address) <= 15
    ), "ip address must be between 7 and 15 characters inclusive"
    ip_address_parts = ip_address.split(".")
    for part in ip_address_parts:
        assert part.isdigit(), "ip address parts must be digits"
        assert (
            0 <= int(part) <= 255
        ), "ip address parts must be between 0 and 255 inclusive"


class IPv4AddressRange:
    def __init__(self, start_ip, end_ip):
        check_is_ipv4_address(start_ip)
        self.start_ip = start_ip
        self.start_ip_parts = tuple(int(i) for i in start_ip.split("."))

        check_is_ipv4_address(end_ip)
        self.end_ip = end_ip
        self.end_ip_parts = tuple(int(i) for i in end_ip.split("."))


def test_ip_v4_address_range():
    start_ip, end_ip = "0.0.0.0", "255.255.255.255"
    ip_address_range = IPv4AddressRange(start_ip, end_ip)
    assert ip_address_range
    assert ip_address_range.start_ip == start_ip
    assert ip_address_range.start_ip_parts == tuple(int(i) for i in start_ip.split("."))
    assert ip_address_range.end_ip == end_ip
    assert ip_address_range.end_ip_parts == tuple(int(i) for i in end_ip.split("."))



test_ip_v4_address_range()

# class IPv4Generator:
#     def __init__(self, start_ip="0.0.0.0", end_ip="255.255.255.255"):
#         check_is_ipv4_address(start_ip)
#         self.start_ip = start_ip
#         self.start_ip_parts = tuple(int(i) for i in start_ip.split("."))
#
#         check_is_ipv4_address(end_ip)
#         self.end_ip = end_ip
#         self.end_ip_parts = tuple(int(i) for i in end_ip.split("."))
