from aoc.day16 import part1, part2, hex_to_bin, Packet


def test_part1():
    """
    8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet (version 1) which
    contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum
    of 16.
    620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; each
    sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.
    C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet uses a
    different length type ID. This packet has a version sum of 23. A0016C880162017C3686B18A3D4780 is an operator
    packet that contains an operator packet that contains an operator packet that contains five literal values; it
    has a version sum of 31. \
    """
    assert part1('8A004A801A8002F478') == 16
    assert part1('620080001611562C8802118E34') == 12
    assert part1('C0015000016115A2E0802F182340') == 23
    assert part1('A0016C880162017C3686B18A3D4780') == 31


def test_part2():
    """
    C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
    04005AC33890 finds the product of 6 and 9, resulting in the value 54.
    880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
    CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
    D8005AC2A8F0 produces 1, because 5 is less than 15.
    F600BC2D8F produces 0, because 5 is not greater than 15.
    9C005AC2F8F0 produces 0, because 5 is not equal to 15.
    9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
    """
    assert part2('C200B40A82') == 3
    assert part2('04005AC33890') == 54
    assert part2('880086C3E88112') == 7
    assert part2('CE00C43D881120') == 9
    assert part2('D8005AC2A8F0') == 1
    assert part2('F600BC2D8F') == 0
    assert part2('9C005AC2F8F0') == 0
    assert part2('9C0141080250320F1802104A08') == 1


def test_literal():
    bits = hex_to_bin('D2FE28')
    assert bits == '110100101111111000101000'
    p, remaining = Packet.parse(bits)
    assert p.version == 6
    assert p.type_id == 4
    assert p.value == 2021
    assert remaining == '000'


def test_bit_length_operator():
    bits = hex_to_bin('38006F45291200')
    assert bits == '00111000000000000110111101000101001010010001001000000000'
    p, remaining = Packet.parse(bits)
    assert p.version == 1
    assert p.type_id == 6
    assert list(child.value for child in p.children) == [10, 20]
    assert remaining == '0000000'


def test_packet_length_operator():
    bits = hex_to_bin('EE00D40C823060')
    assert bits == '11101110000000001101010000001100100000100011000001100000'
    p, remaining = Packet.parse(bits)
    assert p.version == 7
    assert p.type_id == 3
    assert list(child.value for child in p.children) == [1, 2, 3]
    assert remaining == '00000'
