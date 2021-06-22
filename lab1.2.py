"""Напишите функцию, которая будет получать на вход число n и возвращать n-ое число Фибоначи.
Считаем, что нулевое и первое число Фибоначи равны 0 и 1, соответственно."""
import sys 

class InputError(Exception):
    pass

def fib(n):
    """Iterative fibonacci algorithm"""
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            n = int(sys.argv[1])
        elif len(sys.argv) > 2:
            raise InputError("Too many arguments")
        else:
            n = int(input("Enter number: "))
        if n < 0:
            raise ValueError() 
    except:
        print("Invalid argument")
        exit()
    print(fib(n))
