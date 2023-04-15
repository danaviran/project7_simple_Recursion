##############################################################################
# FILE: ex7.py
# WRITERS: Dana Aviran, 211326608, dana.av
# EXERCISE: Intro2cs2 ex7 2021-2022
# DESCRIPTION: Recursive functions
# SITES I USED: https://pythonshowcase.com/question/python-deep-copy-a-list-into-itself-n-times-recursively
##############################################################################


from typing import Any, List, Union
from ex7_helper import *


def mult(x: float, y: int) -> float:
    # this function gets a float number x and an int number y (un-negative)
    # and returns the calculation of x * y
    if y == 1:
        return x
    else:
        return add(mult(x, subtract_1(y)), x)


def is_even(n: int) -> bool:
    # this function gets an (un-negative) int number n and returns True if
    # the number is even and False if it is odd
    if n == 0:
        return True
    if n == 2:
        return True
    if n == 1:
        return False
    else:
        return is_even(subtract_1(subtract_1(n)))


def log_mult(x: float, y: int) -> float:
    # this function is same as the first one, but it's run time is O(log(n))
    if y == 0:
        return 0
    if y == 1:
        return x
    elif not is_odd(y):
        x = add(log_mult(x, divide_by_2(y)), log_mult(x, divide_by_2(y)))
        return x
    elif is_odd(y):
        x = add(x, -1)
        x = add(x,
                add(log_mult(x, divide_by_2(y)), log_mult(x, divide_by_2(y))))
    return x


def is_power_helper(power_of_b: int, x: int, b: int) -> bool:
    # this function is same as the original, but takes also the original value
    # of b as the last argument so we can multiply the new calculation with it
    if x < power_of_b:
        return False
    if x == power_of_b:
        return True
    else:
        power_of_b = int(mult(power_of_b, b))
        return is_power_helper(power_of_b, x, b)


def is_power(b: int, x: int) -> bool:
    # this function gets two int numbers b and x (un-negative) and returns
    # True is there is an un-negative int number n that operates as:
    # b ^ n = x, and returns False if there isn't
    if x == 1:
        return True
    if x == 0:
        if b == 0:
            return True
        else:
            return False
    return is_power_helper(b, x, b)


def string_len(s: str, new_s: str = "", counter: int = 0) -> int:
    # this function gets a string and returns the string length
    if new_s == s:
        return counter
    else:
        new_s = append_to_end(new_s, s[counter])
        return string_len(s, new_s, counter + 1)


def reverse_helper(s: str, length: int, new_str: str = "", i: int = 0) -> str:
    # this function gets a string, the length of it, a new empty string and an
    # index and returns the new string as the reversed original string
    if i < length:
        new_str = append_to_end(new_str, s[length - 1 - i])
        return reverse_helper(s, length, new_str, i + 1)
    else:
        return new_str


def reverse(s: str) -> str:
    # this function gets a string and returns its reversed string
    length = string_len(s)  # we check the length of the string
    return reverse_helper(s, length)


def play_hanoi(Hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> None:
    if n <= 0:
        return
    elif n > 0:
        play_hanoi(Hanoi, n - 1, src, temp, dst)
        Hanoi.move(Hanoi, src, dst)
        play_hanoi(Hanoi, n - 1, temp, dst, src)


def number_of_ones_in_number(n: int, count1: int = 0) -> int:
    # this function gets an int number and returns the num of 1 digits it has
    if n == 1:
        return count1 + 1
    if n == 0:
        return count1
    if n % 10 == 1:
        return number_of_ones_in_number(n // 10, count1 + 1)
    else:
        return number_of_ones_in_number(n // 10, count1)


def number_of_ones_caller(n: int, count2: int = 0) -> int:
    # this function calls the number_of_ones_in_number function and according
    # to the current n value and adds its return value to the count.
    # than, it calls itself recursively and checks the next (n-1) value
    if n > 0:
        count2 += number_of_ones_in_number(n)
        return number_of_ones_caller(n - 1, count2)
    else:
        return count2


def number_of_ones(n: int) -> int:
    # this is the main function. it calls the caller function that acts as
    # a double counter
    if n <= 0:
        return 0
    return number_of_ones_caller(n)


def len_of_list(lst: Union[List[List[int]], List[int]]) -> int:
    # this function gets a list and returns its length (int)
    if lst:
        return 1 + len_of_list(lst[1:])
    else:
        return 0


def compare_outer_index(l1: List[List[int]], l2: List[List[int]], length: int,
                        i: int = 0) -> bool:
    # this function gets two lists and returns True if there the same.
    if i < length:
        length_inner = len_of_list(l1[i])
        if length_inner != len_of_list(l2[i]):  # if the lengths of inner lists
            # is different, we return False
            return False
        elif length_inner == 0:  # if the length is zero, we continue with
            # another call of the function, to the next outer index
            return compare_outer_index(l1, l2, length, i + 1)
        else:
            # if the length is more than zero, we compare the inner value of
            # the inner list by calling the inner function, and call this
            # outer function again to continue to the next index
            return compare_inner_index(l1, l2, length_inner, i) and \
                   compare_outer_index(l1, l2, length, i + 1)
    else:
        return True


def compare_inner_index(l1: List[List[int]], l2: List[List[int]],
                        length_inner: int, i: int = 0, j: int = 0) -> bool:
    # this is the inner function - it checks if every value in the inner list
    # is the same, and if it is, it call itself with the next value
    if j < length_inner:
        if l1[i][j] == l2[i][j]:
            return compare_inner_index(l1, l1, length_inner, i, j + 1)
        else:
            return False
    else:
        return True


def compare_2d_lists(l1: List[List[int]], l2:  List[List[int]]) -> bool:
    # this function gets two lists and returns True if they are the same
    # and false if they aren't
    length = len_of_list(l1)  # we calculate the length using an helper func
    if length != len_of_list(l2):
        return False
    else:
        return compare_outer_index(l1, l2, length)


def magic_list(n: int) -> List[Any]:
    # this function gets an un-negative int number n and makes a list of lists.
    # this recursive function calls itself until it gets to the value zero.
    # when it does, the magic_list call returns [], and the [magic_list] one
    # returns [[]]. then, every magic_list call that got an n value that is
    # positive gets (from the former returns) the value of the n first inner
    # lists, an the second call of the [magic_list] gets all these lists inside
    # a new list. this new list is actually the value of the next index in the
    # outer list.
    if n <= 0:
        return []
    else:
        return magic_list(n - 1) + [magic_list(n - 1)]
