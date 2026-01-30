import pytest

def test_equal_or_not_equal():
    assert 3 == 3

def test_instances():
    assert isinstance('hello world', str)
    assert isinstance(10, int)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type(3.14) is float
    assert type([1, 2, 3]) is list

def test_comparision():
    assert 7 > 3
    assert 4 < 10

def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 is not num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name:str, last_name:str, major:str, year:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year

@pytest.fixture
def default_employee():
    return Student('john', 'doe', 'computer science', 3)

def test_getuser(default_employee):
    assert default_employee.first_name == 'john'
    assert default_employee.last_name == 'doe'
    assert default_employee.major == 'computer science'
    assert default_employee.year == 3
        
