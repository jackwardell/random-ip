from ipaddress import AddressValueError
from ipaddress import IPv4Address
from ipaddress import NetmaskValueError
from ipaddress import summarize_address_range


class IPv4AddressRange:
    def __init__(self, start_ip, end_ip):
        try:
            self._start_ip = IPv4Address(start_ip)
            self._end_ip = IPv4Address(end_ip)

            self.start_ip = self._start_ip.exploded
            self.end_ip = self._end_ip.exploded
        except (AddressValueError, NetmaskValueError):
            raise ValueError(f"{start_ip} is not a valid IPv4 address")

        assert (
            self._start_ip < self._end_ip
        ), "end ip address must be greater than start ip address"

        self.ip_range = range(int(self._start_ip), int(self._end_ip) + 1)

    def count(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return self.ip_range.count(int(_ip_address))

    def index(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return self.ip_range.index(int(_ip_address))

    def to_cidr(self):
        return [
            i.exploded for i in summarize_address_range(self._start_ip, self._end_ip)
        ]

    def __contains__(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return int(_ip_address) in self.ip_range

    def __eq__(self, ip_address_range):
        if not isinstance(ip_address_range, IPv4AddressRange):
            return False
        else:
            return self.ip_range == ip_address_range.ip_range

    def __getitem__(self, item):
        return self.ip_range[item]

    def __repr__(self):
        return f"IPv4AddressRange(start_ip_address={self.start_ip}, end_ip_address={self.end_ip})"

    def __str__(self):
        return f"{self.start_ip} - {self.end_ip}"




# class IPv4Generator:
#     def __init__(self, ranges=None):
#         if ranges:
#
#         self.ranges = ranges
#         check_is_ipv4_address(start_ip)
#         self.start_ip = start_ip
#         self.start_ip_parts = tuple(int(i) for i in start_ip.split("."))
#
#         check_is_ipv4_address(end_ip)
#         self.end_ip = end_ip
#         self.end_ip_parts = tuple(int(i) for i in end_ip.split("."))
