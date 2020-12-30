import collections
import string
from datetime import datetime
from functools import wraps
from ipaddress import IPv6Address, IPv4Address
from logging import Logger
from random import randint, uniform, choices, random, getrandbits
from typing import Callable, Optional, List, Any, Dict

import names

from easy_telegram.util.utils import get_logger


def _unique(func: Callable[[Optional[List[Any]], Optional[Dict[Any, Any]]], Any]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "unique" not in kwargs or not kwargs["unique"]:
            return func(*args, **kwargs)

        func_name: str = func.__name__
        self: Randomizer = args[0]
        _logger: Logger = getattr(self, "_logger")
        _uniques: Dict[str, List] = getattr(self, "_uniques")

        x = func(*args, **kwargs)
        iteration: int = 0
        while x in _uniques[func_name]:
            if iteration > 1000:
                _logger.warning(
                    f"Tried 1000 times to get a new unique value for {func_name}. Maybe in the given limitations there is no more unique value")
                return x
            x = func(*args, **kwargs)
        _uniques[func_name].append(x)
        return x

    return wrapper


class Randomizer:
    _uniques: Dict[str, List[int]]
    _logger: Logger

    def __init__(self):
        self._logger = get_logger(str(type(self)))
        self._uniques = collections.defaultdict(list)

    @_unique
    def random_int(self, min: int, max: int, unique: bool = False) -> int:
        assert min < max, "min cant be smaller than max"
        return randint(min, max)

    @_unique
    def random_float(self, min: float, max: float, unique: bool = False) -> float:
        assert min < max, "min cant be smaller than max"
        return uniform(min, max)

    @_unique
    def random_str(self, length: int, chars: str = None, upper_case: bool = True, lower_case: bool = True,
                   digits: bool = True, special_cars: bool = True, unique: bool = False) -> str:
        assert chars or upper_case or lower_case or digits or special_cars, "A random string option ['upper_case', 'lower_case', 'digits', 'special_chars'] or a given string must be given"

        if not chars:
            chars: List[str] = []
            if lower_case:
                chars.extend(string.ascii_lowercase)
            if upper_case:
                chars.extend(string.ascii_uppercase)
            if digits:
                chars.extend(string.digits)
            if special_cars:
                chars.extend(string.punctuation)

        return ''.join(choices(chars, k=length))

    @_unique
    def random_time(self, min: datetime, max: datetime, unique: bool = False):
        return min + random() * (max - min)

    @staticmethod
    def random_bool(true_probability: float = 0.5) -> bool:
        assert 0 <= true_probability <= 1, f"'true_probability' has to be a value between 0 and 1"
        return random() < true_probability

    @_unique
    def random_ip(self, ip_v6: bool = False) -> str:
        if ip_v6:
            bits = getrandbits(128)
            addr = IPv6Address(bits)
            return addr.exploded
        else:
            bits = getrandbits(32)
            addr = IPv4Address(bits)
            return str(addr)

    @_unique
    def get_name(self, gender: str = None, unique: bool = False) -> str:
        return names.get_full_name(gender=gender)

    @_unique
    def first_name(self, gender: str = None, unique: bool = False) -> str:
        return names.get_first_name(gender=gender)

    @_unique
    def last_name(self, unique: bool = False) -> str:
        return names.get_last_name()
