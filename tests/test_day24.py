from aoc.day24 import Execution

# An ALU program which takes an input number, negates it, and stores it in x.
negation_program = """inp x
mul x -1
"""

# An ALU program which takes two input numbers, then sets z to 1 if the second input number is three times larger than
# the first input number, or sets z to 0 otherwise.
is_three_times_larger_program = """inp z
inp x
mul z 3
eql z x
"""

# An ALU program which takes a non-negative integer as input, converts it into binary, and stores the lowest (1's)
# bit in z, the second-lowest (2's) bit in y, the third-lowest (4's) bit in x, and the fourth-lowest (8's) bit in w.
int_to_binary_program = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""


def test_negation_program():
    instructions = negation_program.splitlines()
    assert Execution(instructions, "1").execute().get('x') == -1
    assert Execution(instructions, "4").execute().get('x') == -4
    assert Execution(instructions, "0").execute().get('x') == 0


def test_is_three_times_larger_program():
    instructions = is_three_times_larger_program.splitlines()
    assert Execution(instructions, "13").execute().get('z') == 1
    assert Execution(instructions, "39").execute().get('z') == 1
    assert Execution(instructions, "78").execute().get('z') == 0
    assert Execution(instructions, "33").execute().get('z') == 0


def test_int_to_binary_program():
    instructions = int_to_binary_program.splitlines()
    assert Execution(instructions, "0").execute() == {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    assert Execution(instructions, "1").execute() == {'w': 0, 'x': 0, 'y': 0, 'z': 1}
    assert Execution(instructions, "2").execute() == {'w': 0, 'x': 0, 'y': 1, 'z': 0}
    assert Execution(instructions, "7").execute() == {'w': 0, 'x': 1, 'y': 1, 'z': 1}
    assert Execution(instructions, "9").execute() == {'w': 1, 'x': 0, 'y': 0, 'z': 1}
