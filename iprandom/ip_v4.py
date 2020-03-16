import bisect
import random
from ipaddress import AddressValueError
from ipaddress import IPv4Address
from ipaddress import IPv4Network
from ipaddress import NetmaskValueError
from ipaddress import summarize_address_range
from collections import Sequence
from collections import Container
from ipaddress import _IPv4Constants


class Ranges(Sequence, Container):
    """

    """

    def __init__(self, *ranges):
        if not ranges:
            raise TypeError("__init__() missing at least 2 required ranges")
        self._boundaries_and_ranges = {}
        for range_ in ranges:
            if not isinstance(range_, range):
                raise ValueError("Ranges only accepts range objects")
            else:
                last_value = max(self._boundaries_and_ranges.keys(), default=0)
                self._boundaries_and_ranges[last_value + len(range_)] = range_
        self._sorted_boundaries = sorted(self._boundaries_and_ranges.keys())

    @classmethod
    def from_iterable(cls, iterable):
        return cls(*iterable)

    def __len__(self):
        return sum([len(r) for r in self._boundaries_and_ranges.values()])

    def __getitem__(self, index):
        if abs(index) > len(self):
            raise IndexError("index out of range")
        else:
            if index < 0:
                index = len(self) + index
            boundaries_index = bisect.bisect(self._sorted_boundaries, index)
            key = self._sorted_boundaries[boundaries_index]
            return self._boundaries_and_ranges[key][index - key]

    def __contains__(self, item):
        for r in self._boundaries_and_ranges.values():
            if item in r:
                return True
            else:
                continue
        return False


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

        self._ip_range = range(int(self._start_ip), int(self._end_ip) + 1)

    def count(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return self._ip_range.count(int(_ip_address))

    def index(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return self._ip_range.index(int(_ip_address))

    def to_cidr(self):
        return [
            i.exploded for i in summarize_address_range(self._start_ip, self._end_ip)
        ]

    def __contains__(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return int(_ip_address) in self._ip_range

    def __eq__(self, ip_address_range):
        if not isinstance(ip_address_range, IPv4AddressRange):
            return False
        else:
            return self._ip_range == ip_address_range._ip_range

    def __getitem__(self, item):
        return self._ip_range[item]

    def __repr__(self):
        return f"IPv4AddressRange(start_ip_address={self.start_ip}, end_ip_address={self.end_ip})"

    def __str__(self):
        return f"{self.start_ip} - {self.end_ip}"


class IPv4Generator:
    def __init__(self, included_ranges=None):
        self.included_ranges = []
        if included_ranges:
            self._store_ranges(included_ranges)
        else:
            self.included_ranges = [range(0, 4294967295)]

        self.ip_choices = Ranges.from_iterable(
            [included_range for included_range in self.included_ranges]
        )

    def _store_ranges(self, ip_address_ranges):
        for ip_address_range in ip_address_ranges:
            if isinstance(ip_address_range, IPv4AddressRange):
                self.included_ranges.append(ip_address_range._ip_range)
            elif isinstance(ip_address_range, IPv4Network):
                self.included_ranges.append(
                    range(
                        int(ip_address_range.network_address),
                        int(ip_address_range.broadcast_address),
                    )
                )
            elif isinstance(ip_address_range, tuple):
                self.included_ranges.append(
                    IPv4AddressRange(*ip_address_range)._ip_range
                )
            else:
                raise ValueError(
                    "The keyword argument ip_address_ranges must be a iterable "
                    "with a length of at least 1. Items in the iterable must be "
                    "a IPv4AddressRange, a IPv4Network (from ipaddress) or a "
                    "tuple with start IP address and end IP address or a mixture."
                )

    def __call__(self):
        return IPv4Address(random.choice(self.ip_choices)).exploded
