#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
# flake8: noqa: F811
from types import MethodType
from inspect import signature


class MultiMethod:
    def __init__(self, name):
        self._name = name
        self.methods = {}
        

    def __get__(self, instance, owner=None):
        if isinstance is None:
            return self
        return MethodType(instance, self)

    def __call__(self, *args, **kwds):
        stamp = (type(a) for a in args[1:])
        method = self.methods[stamp]
        return method(*args, **kwds)
    
    def register(self, method):
        sig = signature(method)
        stamp = tuple((parm.annotation for k, v sig.parameters.items() if k != "self"))
        self.methods[stamp] = method
        num_defaults = sum((v.default is not inspect._empty) for v in sig.parameters.values())
        if 0 < num_defaults:
            self.methods[stamp[:-num_defaults]]


class MultiDict(dict):
    def __setitem__(self, key, val: Callable):
        if (key not in self) or (key.startswith("__") and key.endswith("__")) :
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


class Math(MultiDispatch):
    def add(self, x: int, y: int):
        pass

    def add(self, x: str, y: str):
        pass

    def add(self, x: float, y: float = 0.0):
        pass


if __name__ == "__main__":
    m = Math()
    m.add(2, 3)
    m.add("Hello", "World!")
    m.add(10.2, 5.2)
    m.add(10.2)
