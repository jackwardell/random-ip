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
        (
            self.start_ip_a,
            self.start_ip_b,
            self.start_ip_c,
            self.start_ip_d,
        ) = self.start_ip_parts

        check_is_ipv4_address(end_ip)
        self.end_ip = end_ip
        self.end_ip_parts = tuple(int(i) for i in end_ip.split("."))
        (
            self.end_ip_a,
            self.end_ip_b,
            self.end_ip_c,
            self.end_ip_d,
        ) = self.end_ip_parts
        self.check_end_ip_is_greater_than_start_ip()

        self.ip_a_range = range(self.start_ip_a, self.end_ip_a + 1)

    def check_end_ip_is_greater_than_start_ip(self):
        assert (
            self.start_ip != self.end_ip
        ), "start and end ips match - ip ranges should not match"
        assert (
            self.start_ip_a <= self.end_ip_a
        ), "end ip must be greater than or equal to the start ip"
        if self.start_ip_a == self.end_ip_a:
            assert (
                self.start_ip_b <= self.end_ip_b
            ), "end ip must be greater than or equal to the start ip"
            if self.start_ip_b == self.end_ip_b:
                assert (
                    self.start_ip_c <= self.end_ip_c
                ), "end ip must be greater than or equal to the start ip"
                if self.start_ip_c == self.start_ip_b:
                    assert (
                        self.start_ip_d < self.end_ip_d
                    ), "end ip must be greater than or equal to the start ip"

            # class IPv4Generator:
            #     def __init__(self, start_ip="0.0.0.0", end_ip="255.255.255.255"):
            #         check_is_ipv4_address(start_ip)
            #         self.start_ip = start_ip
            #         self.start_ip_parts = tuple(int(i) for i in start_ip.split("."))
            #
            #         check_is_ipv4_address(end_ip)
            #         self.end_ip = end_ip
            #         self.end_ip_parts = tuple(int(i) for i in end_ip.split("."))
