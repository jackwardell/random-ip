import bisect
import random
from collections import Container
from collections import Sequence
from ipaddress import AddressValueError
from ipaddress import IPv4Address
from ipaddress import IPv6Address
from ipaddress import NetmaskValueError
from ipaddress import summarize_address_range


class _Ranges(Sequence, Container):
    """range sequence to implement random.choice which requires __len__ & __getitem__

    used only for range objects e.g. range(start=x, stop=y, step=z)
    where start < step & step = 1

    :param *ranges: range objects
    e.g. _Ranges(range(10, 20), range(50, 60), range(100, 200))
    """

    def __init__(self, *ranges):
        # throw error if no ranges supplied
        if not ranges:
            raise TypeError("__init__() missing at least 2 required ranges")
        # create a dict of ranges
        # where keys are lengths of ranges and values of ranges
        self._boundaries_and_ranges = {}
        # throw errors if not range types
        for range_ in ranges:
            if not isinstance(range_, range):
                raise ValueError("Ranges only accepts range objects")
            else:
                # len keys are cumulative
                # such that if the first range has a length of 20 and the second has 40
                # first key will be 20 and the second 60
                # get the largest key (which will be the last)
                # first value will be 0
                last_value = max(self._boundaries_and_ranges.keys(), default=0)
                # save ranges
                self._boundaries_and_ranges[last_value + len(range_)] = range_
        # sort for later use and for python versions below 3.6
        self._sorted_boundaries = sorted(self._boundaries_and_ranges.keys())

    @classmethod
    def from_iterable(cls, iterable):
        """instantiate class using iterable

        :param iterable: iterable of ranges
        e.g. _Ranges.from_iterable([ranges(10, 20), range(50, 60)])
        """
        return cls(*iterable)

    def __len__(self):
        """implements special method __len__ required by abstract method from Sequence

        done by summing all range lengths
        """
        return sum([len(r) for r in self._boundaries_and_ranges.values()])

    def __getitem__(self, index):
        """implements special method __len__ required by abstract method from Sequence

        done by checking which range object an index would fall into

        e.g. if r = _Ranges(range(0, 10), range(50, 100))
             calling r[5] would find that the index falls into range(0, 10)
             then it calls __getitem__ on that range object
             returning range(0, 10)[5]
        """
        # if out of index, raise error
        if abs(index) > len(self):
            raise IndexError("index out of range")
        else:
            # if index is negative just reverse into positive
            if index < 0:
                index = len(self) + index
            boundaries_index = bisect.bisect(self._sorted_boundaries, index)
            key = self._sorted_boundaries[boundaries_index]
            return self._boundaries_and_ranges[key][index - key]

    def __contains__(self, item):
        """implements special method __len__ required by abstract method from Container

        done by checking if the item occurs in any of the ranges
        """
        for r in self._boundaries_and_ranges.values():
            if item in r:
                return True
            else:
                continue
        return False


class _BaseRange(Sequence):
    @property
    def address_cls(self):
        raise NotImplementedError()

    def __init__(self, start_ip, end_ip):
        self._start_ip = self.address_cls(start_ip)
        self._end_ip = self.address_cls(end_ip)
        assert (
            self._start_ip < self._end_ip
        ), "end ip address must be greater than start ip address"
        self.start_ip = self._start_ip.exploded
        self.end_ip = self._end_ip.exploded

    @property
    def int_ip_range(self):
        return range(int(self._start_ip), int(self._end_ip) + 1)

    def count(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return self.int_ip_range.count(int(_ip_address))

    def index(self, ip_address, start=None, stop=None):
        _ip_address = IPv4Address(ip_address)
        return self.int_ip_range.index(int(_ip_address), start=start, stop=stop)

    def to_cidr(self):
        return [
            i.exploded for i in summarize_address_range(self._start_ip, self._end_ip)
        ]

    def __len__(self):
        return len(self.int_ip_range)

    def __getitem__(self, item):
        return self.int_ip_range[item]

    def __contains__(self, ip_address):
        _ip_address = self.address_cls(ip_address)
        return int(_ip_address) in self.int_ip_range

    # def __repr__(self):
    #     return f"{__name__}(start_ip_address={self.start_ip}, end_ip_address={self.end_ip})"

    def __str__(self):
        return f"{self.start_ip} - {self.end_ip}"


class IPv4AddressRange(_BaseRange):
    address_cls = IPv4Address

    def __init__(self, start_ip, end_ip):
        super().__init__(start_ip, end_ip)


class IPv6AddressRange(_BaseRange):
    address_cls = IPv6Address

    def __init__(self, start_ip, end_ip):
        super().__init__(start_ip, end_ip)


# class IPv6AddressRange(Sequence):
#     def __init__(self, start_ip, end_ip):
#
#         self._start_ip = IPv6Address(start_ip)
#         self._end_ip = IPv6Address(end_ip)
#         self.start_ip = self._start_ip.exploded
#         self.end_ip = self._end_ip.exploded
#
#         assert (
#             self._start_ip < self._end_ip
#         ), "end ip address must be greater than start ip address"
#
#         self.int_ip_range = range(int(self._start_ip), int(self._end_ip) + 1)
#
#     def count(self, ip_address):
#         _ip_address = IPv6Address(ip_address)
#         return self.int_ip_range.count(int(_ip_address))
#
#     def index(self, ip_address):
#         _ip_address = IPv6Address(ip_address)
#         return self.int_ip_range.index(int(_ip_address))
#
#     def to_cidr(self):
#         return [
#             i.exploded for i in summarize_address_range(self._start_ip, self._end_ip)
#         ]
#
#     def __contains__(self, ip_address):
#         _ip_address = IPv4Address(ip_address)
#         return int(_ip_address) in self.int_ip_range
#
#     def __eq__(self, ip_address_range):
#         if not isinstance(ip_address_range, IPv4AddressRange):
#             return False
#         else:
#             return self.int_ip_range == ip_address_range.int_ip_range
#
#     def __getitem__(self, item):
#         return self.int_ip_range[item]
#
#     def __repr__(self):
#         return f"IPv4AddressRange(start_ip_address={self.start_ip}, end_ip_address={self.end_ip})"
#
#     def __str__(self):
#         return f"{self.start_ip} - {self.end_ip}"


# class IPv6Generator:
#     def __init__(self, included_ranges=None, excluded=None):
#         self.included_ranges = []
#         if included_ranges:
#             self._store_ranges(included_ranges)
#         else:
#             self.included_ranges = [IPv4AddressRange("0.0.0.0", "255.255.255.255")]
#
#         if excluded:
#             if isinstance(excluded, (str, IPv4Address)):
#                 pass
#             else:
#                 self._store_ranges(excluded)
#
#         self.ip_choices = _Ranges.from_iterable(
#             [included_range.int_ip_range for included_range in self.included_ranges]
#         )
#
#     def _store_ranges(self, ip_address_ranges):
#         for ip_address_range in ip_address_ranges:
#             if isinstance(ip_address_range, IPv4AddressRange):
#                 self.included_ranges.append(ip_address_range)
#             elif isinstance(ip_address_range, IPv4Network):
#                 self.included_ranges.append(
#                     IPv4AddressRange(
#                         ip_address_range.network_address,
#                         ip_address_range.broadcast_address,
#                     )
#                 )
#             elif isinstance(ip_address_range, tuple):
#                 self.included_ranges.append(IPv4AddressRange(*ip_address_range))
#             else:
#                 raise ValueError(
#                     "The keyword argument ip_address_ranges must be a iterable "
#                     "with a length of at least 1. Items in the iterable must be "
#                     "a IPv4AddressRange, a IPv4Network (from ipaddress) or a "
#                     "tuple with start IP address and end IP address or a mixture."
#                 )
#
#     def __call__(self):
#         return IPv4Address(random.choice(self.ip_choices)).exploded
#
#
# class IPv4Generator:
#     def __init__(self, included_ranges=None, excluded=None):
#         self.included_ranges = []
#         if included_ranges:
#             self._store_ranges(included_ranges)
#         else:
#             self.included_ranges = [IPv4AddressRange("0.0.0.0", "255.255.255.255")]
#
#         if excluded:
#             if isinstance(excluded, (str, IPv4Address)):
#                 pass
#             else:
#                 self._store_ranges(excluded)
#
#         self.ip_choices = _Ranges.from_iterable(
#             [included_range.int_ip_range for included_range in self.included_ranges]
#         )
#
#     def _store_ranges(self, ip_address_ranges):
#         for ip_address_range in ip_address_ranges:
#             if isinstance(ip_address_range, IPv4AddressRange):
#                 self.included_ranges.append(ip_address_range)
#             elif isinstance(ip_address_range, IPv4Network):
#                 self.included_ranges.append(
#                     IPv4AddressRange(
#                         ip_address_range.network_address,
#                         ip_address_range.broadcast_address,
#                     )
#                 )
#             elif isinstance(ip_address_range, tuple):
#                 self.included_ranges.append(IPv4AddressRange(*ip_address_range))
#             else:
#                 raise ValueError(
#                     "The keyword argument ip_address_ranges must be a iterable "
#                     "with a length of at least 1. Items in the iterable must be "
#                     "a IPv4AddressRange, a IPv4Network (from ipaddress) or a "
#                     "tuple with start IP address and end IP address or a mixture."
#                 )
#
#     def __call__(self):
#         return IPv4Address(random.choice(self.ip_choices)).exploded
