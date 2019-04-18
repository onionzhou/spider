def chain(*iterables):
    # chain('ABC', 'DEF') --> A B C D E F
    for it in iterables:
        for element in it:
            yield element
import operator
def accumulate(iterable, func=operator.add):
    'Return running totals'
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)

    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        print("element {}".format(element))
        total = func(total, element)
        yield total

def fab(it):
    for i in it:
        yield i

def test():
    s = "abc"
    ss = "def"
    q = accumulate(s)
    for i in q:
        print(i)

if __name__ == "__main__":

    a =fab("asdfg")
    for i in a :
        print(i)