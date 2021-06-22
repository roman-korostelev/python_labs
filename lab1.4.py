"""Реализовать программу сортировки строк файла и создание файла содержащий отсор- тированный файл по строкам, а каждая строка отсортирована по словам.
Использовать для сортировки алгоритм Merge Sort (реализовать его самим).
Важно: у вас есть ограничение по оперативной памяти для программы - 400MB.
А поступающие на сортировку файлы могут весить 1GB. """
import sys
import argparse
from math import log2

def comp(lhs, rhs, file):
    if isinstance(rhs, int):
        return get_current_line(file, lhs) <= get_current_line(file, rhs)
    else:
        return lhs <= rhs


def merge_sort(my_list, file, status, list_size = -2):
    if len(my_list) <= 1:
        return my_list

    if  list_size == -2:
        list_size = len(my_list)
    mid = len(my_list)//2
    left_list = my_list[:mid]
    right_list = my_list[mid:]

    merge_sort(left_list, file, status, list_size)
    merge_sort(right_list, file, status, -1)

    if status and list_size != -1:
        done, full = int(log2(len(my_list))), int(log2(list_size))
        sys.stdout.write('\r')
        sys.stdout.write("[{}] {}%".format('#' * done
                                + ' ' * (full - done), int(done / full * 100)))
        sys.stdout.flush()

    index_left = index_right = index_main = 0

    while index_left < len(left_list) and index_right < len(right_list):
        if comp(right_list[index_right], left_list[index_left], file):
            my_list[index_main] = right_list[index_right]
            index_right += 1
        else:
            my_list[index_main] = left_list[index_left]
            index_left += 1
        index_main += 1

    while index_left < len(left_list):
        my_list[index_main] = left_list[index_left]
        index_left += 1
        index_main += 1

    while index_right < len(right_list):
        my_list[index_main] = right_list[index_right]
        index_right += 1
        index_main += 1


def get_positions(file):
    yield 0
    while file.readline():
        yield file.tell()


def get_current_line(file, pos):
    file.seek(pos)
    return file.readline()


def file_sort(file_in = "test.txt", file_out = "test_out.txt", status = 1):
    name, ext = file_in.rsplit('.')
    temp_filename = name + '_temp.' + ext

    with open(file_in, "r") as file:
        with open(temp_filename, "w") as temp_file:
            for line in file:
                merge_sort(sorted_line := line.split(), temp_file, status)
                temp_file.write(' '.join(sorted_line) + '\n')

    with open(temp_filename, "r") as temp_file:
        with open(file_out, "w", newline="\n") as out_file:
            size = list(get_positions(temp_file))
            if status:
                print()
            merge_sort(size, temp_file, status)
            for num in size:
                out_file.write(get_current_line(temp_file, num))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        args = dict()
        args["file_in"] = input("Enter file_in name?\n>")
        args["file_out"] = input("Enter file_out name?\n>")
        args["status"] = int(input("Are you need statusbar?\n>"))
        file_sort(**args)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--file_in",  nargs='?',
                            default='test.txt', type=str)
        parser.add_argument("--status", nargs='?',
                            type=int, default=1)
        parser.add_argument("--file_out", nargs='?',
                            default='test_out.txt', type=str)
        args = parser.parse_args()
        file_sort(**vars(args))
