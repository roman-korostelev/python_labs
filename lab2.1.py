"""Реализовать функцию, которая на вход принимает объект (класс тоже объект) и какое-либо значение,
а возвращает название атрибута переданного объекта, значение которое равно переданному значению.
По возможности реализовать как можно больше различных спопсобов решения задачи."""
import inspect


def attr_by_value1(obj, val):
    for name in dir(obj):
        if val == getattr(obj, name):
            return name
    return "No attributes with this value :("


def attr_by_value2(obj, val):
    for name, cur_val in inspect.getmembers(obj):
        if not name.startswith('_') and cur_val == val:
            return name
    return "No attributes with this value :("


def attr_by_value3(obj, val):
    for name, cur_val in obj.__dict__.items():
        if not name.startswith('_') and cur_val == val:
            return name
    return "No attributes with this value :("


if __name__ == '__main__':
    print(attr_by_value3(type("A", (), {'a': 2}), 2))
