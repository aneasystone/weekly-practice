from collections.abc import Generator

class DemoGenerator:
    def __init__(self, generator: Generator[str, None, None]):
        self.generator = generator
        self.closed = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.closed:
            raise StopIteration
        try:
            return next(self.generator)
        except Exception:
            self.close()
            raise

    def close(self):
        if not self.closed:
            self.closed = True
            print('Generator is closed')
            if self.generator is not None and hasattr(self.generator, "close"):
                self.generator.close()

def func():
    yield "a"
    yield "b"
    yield "c"

print(type(func()))

def func2():
    yield from func()

items = DemoGenerator(func2())
for item in items:
    print(item)

###

class CountIterator:
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

# 使用迭代器
iterator = CountIterator(1, 3)
    
# # 将迭代器转成生成器
# def func3():
#     yield from iterator
    
# for num in func3():
#     print(num)  # 输出: 1, 2, 3

while True:
    num = next(iterator)
    print(num)