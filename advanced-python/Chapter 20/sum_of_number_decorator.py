""" Implementing caching has a problem when we want to extend the function it will require separate cache. 
We will use memoize decorator. Our decorator will accept function which needs to be memoized as input. 
We will use functools.wrap function when creating decorator. 
This is not mandatory but good practise to ensure documentation and signature of funciton is decorated.
args list is required in this case because function we want to decorate accepts input arguments
"""

import functools

def memoize(fn):
    cache=dict() 

    @functools.wraps(fn)
    def memoizer(*args):
        if args not in cache:
            cache[args]=fn(*args)
        return cache[args]
    
    return memoizer 


@memoize
def number_sum(n):
    """ returns sum of numbers """
    assert (n >=0), "n must be >=0"
    if n==0:
        return 0 
    else:
        return n+number_sum(n-1)

@memoize
def fibonacci_numbers(n): 
    """ return febonacci number of nth position """
    assert (n >=0), "n must be >=0"
    if n in (0,1):
        return n
    else:
        return fibonacci_numbers(n-1) + fibonacci_numbers(n-2)



def main(): 
    from timeit import Timer

    to_execute=[
        (number_sum, Timer("number_sum(30)", """from __main__ import number_sum""")),
        (fibonacci_numbers, Timer("fibonacci_numbers(10)", "from __main__ import fibonacci_numbers"))
    ]

    for item in to_execute:
        fn=item[0]
        t=item[1]
        print(f"Function: {fn.__name__} : {fn.__doc__}")
        print(f"Time: {t.timeit()}")
        print()


if __name__ == "__main__":
    main()