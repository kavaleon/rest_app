def f1(value):
    def wrapper(next_value=None):
        if next_value is None:
            return value
        else:
            return f1(value + next_value)
    return wrapper


print(f1(4)(7)(2)())
print(f1(5)(9)(10)())




