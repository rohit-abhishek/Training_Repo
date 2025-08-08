### This is 4th program to test the benchmark. This program can be used as replacement for IPython file

import timeit

result = timeit.timeit("benchmark()", setup="from particle_benchmark import benchmark", number=10)
print(result)

result = timeit.repeat("benchmark()", setup="from particle_benchmark import benchmark", number=10, repeat=3)
print(result)