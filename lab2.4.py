"""Класс логгер с возможностью наследования. Класс должен логировать то, какие методы и с какими аргументами у него вызывались и какой был результат этого вызова.
Функция str() от класса должна отддавать лог вызовов. Должна быть возможность унаследоваться от такого класса, чтобы добавить логирование вызовов у любого класса.
При формированиие строк использовать механизм format. Механиз работы класса логгера должен быть максимально общим, что позволяет использовать его для любого пользовательнского класса.
ВАЖНО: под возможностью насследоваться имеется в виду, что основное использование логгера будет производиться НЕ через наследование (но возможность должна быть),
а другие механизмы/протоколы языка (какие именно вам необходимо решить сами)."""
class Logger:

    def __init__(self, cls=None):
        self.logs = ""
        self.wrapped = cls

    def __call__(self, *args, **kwargs):
        self.cls = self.wrapped(*args, **kwargs)
        return self

    def __getattribute__(self, item):
        if item in super().__getattribute__('__dict__'):
            return super().__getattribute__(item)
        elif super(Logger, self).__getattribute__('wrapped') is None:
            attr = super().__getattribute__(item)
        else:
            attr = super().__getattribute__('cls').__getattribute__(item)

        def method(*args, **kwargs):
            val = attr(*args, **kwargs)
            log_method = 'The method {} was called '.format(item)
            log_args = 'with args {} '.format(args) if args else 'without args '
            log_kwargs = 'and with kwargs {}. '.format(kwargs) if kwargs else 'and without kwargs. '
            log_ans = 'Result of call: {}\n'.format(val) if not val is None else "It return nothing\n"
            self.logs += log_method + log_args + log_kwargs + log_ans

            return val

        if hasattr(attr, '__call__'):
            return method
        return attr

    def __str__(self):
        return self.logs


class FirstClass(Logger):
    def __init__(self):
        self.a = 12
        super().__init__()

    def some_func(self, a, b=2):
        print(a, b, self.a)
        return 'Hi'


@Logger
class SecondClass:
    def __init__(self):
        self.a = 12
        super().__init__()

    def some_func(self, a, b=2):
        print(a, b, self.a)


first_test = FirstClass()
first_test.some_func(2)
first_test.some_func(5, b = 37)
print(str(first_test))
print()

second_test = SecondClass()
second_test.some_func(34)
second_test.some_func(12, b=55)
print(str(second_test))
