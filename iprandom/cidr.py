def parse_cidr(cidr_value):
    assert isinstance(cidr_value, str), "CIDR must be a string"
    assert "/" in cidr_value, "CIDR must contain a /"
    prefix, bits = cidr_value.split("/")
    bits = int(bits)
    ip_address = tuple(int(i) for i in prefix.split("."))
    return ip_address, bits
