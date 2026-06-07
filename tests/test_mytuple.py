import pytest

from mytuple import Employee, as_csv


@pytest.fixture
def empl():
    return Employee("Alice", "Software Engineer", 70000)


def test_employee_creation(empl):
    assert empl == ("Alice", "Software Engineer", 70000)


def test_employee_properties(empl):
    assert empl.name == "Alice"
    assert empl.position == "Software Engineer"
    assert empl.salary == 70000


def test_as_csv(empl):
    assert as_csv(empl) == "name='Alice', position='Software Engineer', salary=70000"


def test_employee_wrong_number_of_arguments():
    with pytest.raises(TypeError, match=r"^<class 'Employee'>: expects 3 args$"):
        Employee("Software Engineer", 70000)
