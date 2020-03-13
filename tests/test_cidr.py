from iprandom.cidr import parse_cidr


def test_cidr():
    result = parse_cidr('0.0.0.0/0')
    assert result
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], tuple)
    assert isinstance(result[0][0], int)
    assert isinstance(result[0][1], int)
    assert isinstance(result[0][2], int)
    assert isinstance(result[0][3], int)
    assert isinstance(result[1], int)
