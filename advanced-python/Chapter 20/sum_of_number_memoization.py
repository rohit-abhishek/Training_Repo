""" Let's see the improvement using memoization technique. Naive technique took almost 1.53 ms"""
sum_cache={0:0}

def number_sum(n):
    """ Return sum of first n numbers """

    assert (n>=0), "n must be >=0"

    if n in sum_cache:
        return sum_cache[n]

    result= n+number_sum(n-1) 

    sum_cache[n]=result
    return result

""" Proble with this approach is if we want to extend this program for fibonacci series we will have create new cache for febonacci"""
febo_cache={0:0, 1:1}
def febonacci_numbers(n):
    """ return febonacci series up for given numbers"""

    assert (n>=0), "n must be >=0"

    if n in febo_cache:
        return febo_cache[n]

    result=febonacci_numbers(n-1) + febonacci_numbers(n-2)

    febo_cache[n]=result
    
    return result


if __name__ == "__main__":
    from timeit import Timer 
    t=Timer('number_sum(30)', """from __main__ import number_sum""")
    print("Time: ", t.timeit())
    print (sum_cache)

    t=Timer('febonacci_numbers(30)', """from __main__ import febonacci_numbers""")
    print("Time: ", t.timeit())
    print (febo_cache)
