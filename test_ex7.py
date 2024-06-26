from random import randint, random, choice
import sys
import subprocess
from typing import Set
import traceback
from ex7 import magic_list, mult, is_even, log_mult, is_power, compare_2d_lists, reverse, number_of_ones


def generate_letter():
    return chr(randint(ord("A"), ord("z") + 1))


def generate_string(length):
    """Returns new string with different chars"""
    p = set(range(ord("A"), ord("z") + 1))
    s = ""
    for _ in range(length):
        c = chr(choice(list(p)))
        p -= {c}
        s += c
    return s


def test_mult():
    for _ in range(100):
        x = randint(0, 400) + random()
        y = randint(0, 400)
        assert abs(mult(x, y) - x * y) < 0.01


def test_is_even():
    for x in range(100):
        x = randint(0, 400)
        assert is_even(x) == (x % 2 == 0)


def test_log_mult():
    for _ in range(100):
        x = randint(0, 400) + random()
        y = randint(0, 400)
        assert abs(log_mult(x, y) - x * y) < 0.01
    assert abs(log_mult(0.5, 100_000) - 50_000) < 0.01

def test_is_power():
    try:
        assert is_power(0, 0)
    except:
        raise AssertionError("There isn't edge case for is_power(0, 0)!")
    for x in range(20):
        try:
            assert not is_power(randint(1, 1000), 0)
        except:
            raise AssertionError("There isn't edge case for is_power(n, 0)!")
        try:
            assert is_power(randint(1, 1000), 1)
        except:
            raise AssertionError("There isn't edge case for is_power(n, 1)!")

    for _ in range(100):
        b = randint(2, 100)
        x1 = b ** randint(1, 15)
        x2 = b
        while x2 % b == 0 or x2 == 1:
            x2 = b * (randint(0, 1) + random())
            x2 = round(x2)
            x2 = x2 ** randint(1, 15)
        assert is_power(b, x1)
        assert not is_power(b, x2)


def test_reverse():
    assert reverse('') == ''
    assert reverse('a') == 'a'
    assert reverse('ab') == 'ba'
    for _ in range(100):
        _str = generate_string(randint(1, 100))
        assert reverse(_str) == _str[::-1]


def test_number_of_ones():
    try:
        assert number_of_ones(0) == 0 
    except RecursionError:
        raise AssertionError("There isn't edge case for number_of_ones(0)!")
    assert number_of_ones(1) == 1
    assert number_of_ones(10) == 2
    assert number_of_ones(100) == 21
    assert number_of_ones(200) == 20 + 20 + 100


def test_compare_2d_lists():
    assert compare_2d_lists([], [])
    assert not compare_2d_lists([], [[]])
    assert compare_2d_lists([[]], [[]])
    assert not compare_2d_lists([[1]], [[]])
    assert compare_2d_lists([[1]], [[1]])
    assert not compare_2d_lists([[], []], [[]])
    assert not compare_2d_lists([[], []], [[1]])
    assert compare_2d_lists([[], []], [[], []])
    assert compare_2d_lists([[1], []], [[1], []])
    assert not compare_2d_lists([[1], []], [[2], []])
    assert compare_2d_lists([[1], [2, 3]], [[1], [2, 3]])


def collect_deep(iterable, ids: Set[int]):
    for x in iterable:
        assert id(x) not in ids, "There are two references to the same list!"
        ids.add(id(x))
        if isinstance(x, list):
            collect_deep(x, ids)


def test_magic_list():
    ids = set()
    lst = list(map(magic_list, range(10)))
    collect_deep(lst, ids)
    for i, l in enumerate(lst):
        assert lst[:i] == l
    ids.clear()

    i = randint(10, 20)
    l1 = magic_list(i)
    l2 = magic_list(i + 1)
    collect_deep([l1, l2], ids)
    assert l2[:-1] == l1
    assert l2[-1] == l1


class MypyTypesError(Exception):
    def __init__(self, output):
        self.text = "mypy types check returns some errors:"
        errors = "\n\t\t".join(output.split("\n")[:-2])
        self.text += "\n\t\t" + errors

    def __format__(self, _):
        return self.text


def test_mypy_strict():
    mypy = subprocess.run(["mypy", "--strict", "ex7.py"],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')
    if mypy.count("error") != 0:
        raise MypyTypesError(mypy)


def run_test(name, func):
    try:
        func()
        print(f"\033[1;32m{name} test PASSED")
        return 1
    except MypyTypesError as e:
        print(f"\033[1;31m{name} test FAILED\n\t{type(e).__name__}: {e}")
    except Exception as e:
        print(f"\033[1;31m{name} test FAILED\n\t{type(e).__name__}: {e}")
        print(traceback.format_exc())
    return 0


def main():
    tests = [
        "mult",
        "is_even",
        "log_mult",
        "is_power",
        "reverse",
        "number_of_ones",
        "compare_2d_lists",
        "magic_list",
        "mypy_strict"]
    count = 0
    for test in tests:
        count += run_test(test, globals()["test_" + test])
    print()
    if count == len(tests):
        print("\033[1;32m=========All OK=========")
    else:
        print(f"\033[1;31m========={count}/{len(tests)} tests passed=========")
    print("\033[0m")


if __name__ == "__main__":
    sys.exit(int(main() or 0))
