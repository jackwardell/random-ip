# def check_is_ipv4_address(ip_address):
#     assert isinstance(ip_address, str), "ip address must be a string"
#     assert (
#         7 <= len(ip_address) <= 15
#     ), "ip address must be between 7 and 15 characters inclusive"
#     ip_address_parts = ip_address.split(".")
#     for part in ip_address_parts:
#         assert part.isdigit(), "ip address parts must be digits"
#         assert (
#             0 <= int(part) <= 255
#         ), "ip address parts must be between 0 and 255 inclusive"


from ipaddress import IPv4Address


class IPv4AddressRange:
    def __init__(self, start_ip, end_ip):
        self.start_ip = start_ip
        self._start_ip = IPv4Address(start_ip)

        self.end_ip = end_ip
        self._end_ip = IPv4Address(end_ip)

        assert self._start_ip < self._end_ip, "end ip address must be greater than start ip address"

        self.ip_range = range(int(self._start_ip), int(self._end_ip) + 1)

    def __contains__(self, ip_address):
        _ip_address = IPv4Address(ip_address)
        return int(_ip_address) in self.ip_range

    def __eq__(self, ip_address_range):
        if not isinstance(ip_address_range, IPv4AddressRange):
            return False
        else:
            return self.ip_range == ip_address_range.ip_range

# def _check_end_ip_is_greater_than_start_ip(self):
#     end_must_be_greater = "end ip must be greater than or equal to the start ip"
#     assert self.start_ip != self.end_ip, (
#         "start and end ips match - ip ranges should not match "
#         "but rather the end ip should be greater than the start ip"
#     )
#     assert self.start_ip_parts[0] <= self.end_ip_parts[0], end_must_be_greater
#     if self.start_ip_parts[0] == self.end_ip_parts[0]:
#         assert self.start_ip_parts[1] <= self.end_ip_parts[1], end_must_be_greater
#         if self.start_ip_parts[1] == self.end_ip_parts[1]:
#             assert (
#                 self.start_ip_parts[2] <= self.end_ip_parts[2]
#             ), end_must_be_greater
#             if self.start_ip_parts[2] == self.end_ip_parts[2]:
#                 assert (
#                     self.start_ip_parts[3] < self.end_ip_parts[3]
#                 ), end_must_be_greater

# class IPv4Generator:
#     def __init__(self, start_ip="0.0.0.0", end_ip="255.255.255.255"):
#         check_is_ipv4_address(start_ip)
#         self.start_ip = start_ip
#         self.start_ip_parts = tuple(int(i) for i in start_ip.split("."))
#
#         check_is_ipv4_address(end_ip)
#         self.end_ip = end_ip
#         self.end_ip_parts = tuple(int(i) for i in end_ip.split("."))
