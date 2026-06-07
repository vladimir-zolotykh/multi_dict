#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from operator import itemgetter


class TupleMeta(type):
    def __init__(cls, name, bases, clsdict):
        fields = clsdict.get("_fields", [])
        for k, name in enumerate(fields):
            clsdict[name] = property(itemgetter(k))


class MyTuple(tuple, metaclass=TupleMeta):
    def __new__(cls, *args):
        print(len(args))
        return super().__new__(cls, args)


class Employee(MyTuple):
    _fields = ["name", "position", "salary"]


if __name__ == "__main__":
    empl = Employee("Alice", "Software Engineer", 70000)
    print(empl)
