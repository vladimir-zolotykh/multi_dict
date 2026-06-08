#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# flake8: noqa: F811
from typing import Callable, Any, MutableMapping
from types import MethodType
from functools import wraps
from inspect import signature, _empty


class MultiMethod:
    def __init__(self, name):
        self._name = name
        self.methods = {}

    def __get__(self, instance, owner=None):
        if isinstance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, *args, **kwds):
        stamp = tuple(type(a) for a in args)[1:]
        method = self.methods[stamp]
        return method(*args, **kwds)

    def register(self, method):
        sig = signature(method)
        stamp = tuple((v.annotation for v in sig.parameters.values()))[1:]
        self.methods[stamp] = method
        num_defaults = sum(v.default is not _empty for v in sig.parameters.values())
        if 0 < num_defaults:
            self.methods[stamp[:-num_defaults]] = method


class MultiDict(dict):
    def __setitem__(self, key, val: Callable):
        if key.startswith("__") and key.endswith("__"):
            super().__setitem__(key, val)
            return
        if key not in self:
            super().__setitem__(key, val)
            return
        oval: Callable = self[key]
        mm: MultiMethod
        if isinstance(oval, MultiMethod):
            mm = oval
            mm.register(val)
        else:
            mm = MultiMethod(key)
            mm.register(oval)
            mm.register(val)
        super().__setitem__(key, mm)


class MultiDispatch(type):
    @classmethod
    def __prepare__(
        metacls, name: str, bases: tuple[type, ...], /, **kwds: Any
    ) -> MutableMapping[str, object]:
        return MultiDict()


def stamp(func):
    @wraps(func)
    def wrapper(*args, **kwds):
        sig = signature(func)
        # print(list(v.annotation for k, v in sig.parameters.items() if k != "self"))
        print(f"{func.__name__} {sig}")
        res = func(*args, **kwds)
        return res

    return wrapper


class Math(metaclass=MultiDispatch):
    def add(self, x: int, y: int):
        print(f"add-int-int({x}, {y})")

    def add(self, x: str, y: str):
        print(f"add-str-str({x}, {y})")

    def add(self, x: float, y: float = 0.0):
        print(f"add-float-float({x}, {y})")


if __name__ == "__main__":
    m = Math()
    m.add(2, 3)
    m.add("Hello", "World!")
    m.add(10.2, 5.2)
    m.add(10.2)
