"""Реализовать полностью свой (наследоваться нельзя, использовать встроенный range нельзя;
все должно быть написанно с нуля) класс range с аналогичным встроенному интерфейсом и функциональностью.
Однако ваш range должен поддерживать механизм фильтрации, то есть при передачи функции-фильтра значения будут фильтроваться (как если бы мы использоваль filter над range; filter использовать нельзя.)
(если функция-фильтр не передана, то работает как обычный range)"""
class Range:
    def __init__(self, start, end=None, step=1, my_filter=None):
        if step == 0:
            raise ValueError
        if end is None:
            self.end = start
            self.start = 0
        else:
            self.start = start
            self.end = end
        self.step = step

        for arg in (self.start, self.end, self.step):
            if not isinstance(arg, int):
                raise ValueError

        if my_filter is None:
            self.filter = lambda x: True
        else:
            self.filter = my_filter

    def __iter__(self):
        cur_val = self.start

        def comp():
            return cur_val < self.end if self.step > 0 else cur_val > self.end
        while comp():
            if self.filter(cur_val):
                yield cur_val
            cur_val += self.step


for i in Range(2, 10, 3, lambda x : x % 2):
    print(i)


for i in Range(10, my_filter= lambda x : x % 3 == 0):
    print(i, end=' ')
print()


for i in Range(25):
    print(i, end=' ')
print()


for i in Range(10, 15, 2):
    print(i, end=' ')
print()


try:
    for i in Range(10.5):
        print(i, end=' ')
except ValueError:
    print('Oops, wrong argument :(')

