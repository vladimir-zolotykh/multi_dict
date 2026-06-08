# test_multidispatch.py

import pytest

from multi_method import Math, MultiMethod


def test_add_is_multimethod():
    assert isinstance(Math.__dict__["add"], MultiMethod)


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ((2, 3), "add (x: int, y: int) (2, 3)"),
        (("Hello", "World!"), "add (x: str, y: str) ('Hello', 'World!')"),
        ((10.2, 5.2), "add (x: float, y: float = 0.0) (10.2, 5.2)"),
        ((10.2,), "add (x: float, y: float = 0.0) (10.2,)"),
    ],
)
def test_dispatch(capsys, args, expected):
    m = Math()

    m.add(*args)

    out = capsys.readouterr().out.strip()
    assert out == expected


def test_unknown_signature_raises_keyerror():
    m = Math()

    with pytest.raises(KeyError):
        m.add(1, "abc")


def test_method_is_bound_to_instance():
    m = Math()

    bound = m.add

    assert callable(bound)

    # If binding works, invocation succeeds.
    bound(2, 3)


def test_default_argument_registration(capsys):
    m = Math()

    m.add(10.2)

    out = capsys.readouterr().out.strip()

    assert "float" in out
    assert "(10.2,)" in out
