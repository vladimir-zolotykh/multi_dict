#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> empl = Employee("Alice", "Software Engineer", 70000)
>>> empl
('Alice', 'Software Engineer', 70000)
>>> as_csv(empl)
"name='Alice', position='Software Engineer', salary=70000"
>>> empl = Employee("Software Engineer", 70000)
Traceback (most recent call last):
...
TypeError: <class 'Employee'>: expects 3 args
"""
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, name, bases, clsdict):
        fields = clsdict.get("_fields", [])
        for k, name in enumerate(fields):
            setattr(cls, name, property(itemgetter(k)))


class MyTuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        if len(args) != (n := len(cls._fields)):
            raise TypeError(f"<class {cls.__name__!r}>: expects {n} args")
        return super().__new__(cls, args)


class Employee(MyTuple):
    _fields = ["name", "position", "salary"]


def as_csv(empl: Employee) -> str:
    return ", ".join(f"{n}={getattr(empl, n)!r}" for n in empl._fields)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
