from multi_method import MultiDispatch


class Calculator(metaclass=MultiDispatch):
    def add(self, x: int, y: int):
        return x + y

    def add(self, x: str, y: str):
        return f"{x} {y}"

    def add(self, x: float, y: float = 0.0):
        return x + y


def test_int_dispatch():
    c = Calculator()
    assert c.add(2, 3) == 5


def test_str_dispatch():
    c = Calculator()
    assert c.add("Hello", "World") == "Hello World"


def test_float_dispatch():
    c = Calculator()
    assert c.add(1.5, 2.5) == 4.0


def test_float_default_dispatch():
    c = Calculator()
    assert c.add(1.5) == 1.5
