"""Реализовать функцию преобразования объекта в XML-строку.
На вход функции подается питоновский объект: int, float, str, dict, set, list, tuple.
На выходе получаем строку или файл."""
import sys
import argparse

def check(obj):
    try:
        int(obj)
    except:
        False
    else:
        return isinstance(obj, str)


def object_to_xml(obj, level=0, member=False, dict_member=False):
    """Recursive function to get xml"""
    obj_type = obj.__class__.__name__
    if not member and not dict_member and not hasattr(obj, "__iter__"):
        start = f'<obj type={obj_type}>'
        end = f'</obj>'
    elif dict_member:
        start = f"<item key='{str(obj[0])}'>"
        end = f"</item>"
    elif member:
        start = '<item>' if not check(obj) else "<item type='str'>"
        end = '</item>'
    else:
        start = f'<{obj_type}>'
        end = f'</{obj_type}>'
    level_t = '\t' * level
    if not hasattr(obj if not dict_member else obj[1], "__iter__") or isinstance(obj if not dict_member else obj[1], str):
        return level_t + start + str(obj if not dict_member else obj[1]) + end + '\n'
    else:
        if member or dict_member:
            return level_t + start + '\n' + object_to_xml(obj[1] if dict_member else obj, level + 1, False, False) + level_t + end + '\n'
        else:
            ans = ''
            iter = obj if not isinstance(obj, dict) else obj.items()
            d = isinstance(obj, dict)
            for item in iter:
                ans += object_to_xml(item, level + 1, not d, d)
            return level_t + start + '\n' + ans + level_t + end + '\n'


if __name__ == "__main__":
    if len(sys.argv) == 1:
        file_in = input("Enter file_in name:\n>")
        file_out = input("Enter file_out name:\n>")
        with open(file_in, "r") as f:
            obj = eval(f.readline())
        with open(file_out, "w") as f:
            f.write(object_to_xml(obj))
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--file_in", nargs='?',
                            default='obj.txt', type=str)
        parser.add_argument("--file_out", nargs='?',
                            default='obj.xml', type=str)
        args = vars(parser.parse_args())
        with open(args["file_in"], "r") as f:
            obj = eval(f.readline())
        with open(args["file_out"], "w") as f:
            f.write(object_to_xml(obj))



