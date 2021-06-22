"""Реализовать программу генерирующую текстовый файл. Основными параметрами по которым генерируется файл являются:

    size - размер в мегабайтах выходного файла;
    symbols - разрешенные символы для генерации, то есть только такие символы могут быть использованны для генерации файла.
    параметр может принимать только следующие значения: digits, latin, cyrillic, utf-8. По умолчанию используется - latin.
    line - это tuple или int. Если параметр равен конкретному числу, то в каждой страке файла должно находиться ровно такое число слов (за исключением последней, почему? подумайте сами).
    Если tuple, то там содержаться два числа и количество слов в строке является случайным силом на этом промежутке. По умолчанию - (10, 50)
    word - аналогично line, только ограничения на длину слова. По умолчанию - (5, 9).

Замечание: файл по суте сотоит из слов, слова не могут содержать пробельных символов (таб, пробел и тд). Слова могут быть разделены только ОДНИМ пробельным символом."""
from random import randint
import argparse
import sys
from platform import system

symbols_dict = {            # ranges for symbols
    'latin': (97, 122),
    'cyrilic': (1072, 1105),
    'digits': (48, 57),
    "utf-8": (0, 1114110)
}

mb_size = 1_048_576 if system() == 'Windows' else 1_000_000    # mb size depending on system


def my_random(a, b):
    """random without whitespace code and utf-8 surrogates"""
    if not chr(ans := randint(a, b)).isspace():
        try:
            chr(ans).encode()
        except UnicodeEncodeError:
            return my_random(a, b)
        return ans
    else:
        return my_random(a, b)


def get_size(s: str):
    """function for getting size of string in bytes"""
    return len(s.encode("utf-8"))


def get_word(symbols, word):
    """generation of word"""
    return ''.join([chr(my_random(*symbols_dict[symbols])) for _ in range(randint(*word))])


def get_line(symbols, line, word):
    """generation of line"""
    words = []
    for _ in range(1, randint(*line)):
        words.append(get_word(symbols, word))
    return ' '.join(words) + '\n'


def into_tuple(arg):
    """from int to tuple with two same values"""
    return arg if isinstance(arg, tuple) else tuple([arg]*2)


def show_status(size, size_left):
    """"show status of task"""
    complete = int((size*mb_size - size_left)/(size*mb_size) * 50)
    incomplete = 50 - complete
    print("[{}] {}%".format('#'*complete + ' '*incomplete,
                            int((size*mb_size - size_left) / (size*mb_size) * 100)), end='\r')


def gen_lines(size, symbols='latin', line=(10, 50), word=(5, 9), status=True):
    """lines generator"""
    line, word = into_tuple(line), into_tuple(word)

    size_left = size * mb_size
    while size_left > 0:
        yield (cur_line := get_line(symbols, line, word).encode()[:size_left])
        size_left -= len(cur_line)
        if status:
            show_status(size, size_left)


def generate_file(size: float, symbols: str = 'latin',
                  line: tuple = (10, 50), word: tuple = (5, 9),
                  status=True, file_path='test.txt'):
    """file generator"""
    with open(file_path, 'w+b') as f:
        f.writelines(gen_lines(size, symbols, line, word, status))


def arg_check(val):
    """function for making tuple or int for args"""
    if len(val) == 1:
        return val[0]
    else:
        return tuple(val)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        args = dict()
        print("Enter values of args."
              " If arg is tuple, enter two numbers separated by comma")
        args["size"] = int(input("Size: "))
        args["symbols"] = input("Symbols: ")
        temp = input("Line: ").split(',')
        args["line"] = int(temp[0]) if len(temp) == 1 else tuple(map(int, temp))
        temp = input("Word: ").split(',')
        args["word"] = int(temp[0]) if len(temp) == 1 else tuple(map(int, temp))
        print("Show status bar?\n"
              "1.Yes\n"
              "2.No")
        args["status"] = input('>') == '1'
        print("Do you want to point a file path?\n"
              "1.Yes\n"
              "2.No")
        args["file_path"] = input("Enter file path: ") if input(">") == '1' else 'test.txt'
        generate_file(**args)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--size", type=int)
        parser.add_argument("--symbols", nargs='?',
                            default='latin', type=str)
        parser.add_argument("--line", nargs='+',
                            default=(10, 50), type=int)
        parser.add_argument("--word", nargs='+',
                            default=(5, 9), type=int)
        parser.add_argument("--status", nargs='?',
                            type=int, default=1)
        parser.add_argument("--file_path", nargs='?',
                            default='test.txt', type=str)
        args = parser.parse_args()
        args.word = arg_check(args.word)
        args.line = arg_check(args.line)
        generate_file(**vars(args))
