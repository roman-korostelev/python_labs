"""Реализовать свой класс-аналог defaultdict, который позволяет рекурсивно читать и записывать значения в виде d['a']['b']['c'] = 1
(даже если изначально d был пустым), а при вызове str(d) выводит данные как словарь в текстовом виде."""
class DefaultDict(dict):
    def __getitem__(self, item):
        if self.get(item) is None:
            self[item] = DefaultDict()
        return self.get(item)


if __name__ == "__main__":
    ExampleDict = DefaultDict()
    ExampleDict["FirstExampleValue"]["SecondExampleValue"] = "SomeRandomValue"
    ExampleDict["FirstExampleValue"]["ThirdExampleValue"] = "AlsoSomeRandomValue"
    TestOfDefaultValue = ExampleDict["FirstExampleValue"]["FourthExampleValue"]["ThirdExampleValue"] == DefaultDict()
    print(ExampleDict, TestOfDefaultValue, sep='\n')
