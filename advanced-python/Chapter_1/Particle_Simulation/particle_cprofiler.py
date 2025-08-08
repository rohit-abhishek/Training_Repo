#### This is 7th code in the whole series 

#### After evaluating execution time; we can make use of profiler utility to tune the performance of the system 
#### there are 2 profilers available - 
#### a. Standard profiler - written in python. Vast platform support 
#### b. cProfiler - written in C, smaller overhead to system. Sutiable for general purpose 
#### 
#### 1. Running cprofiler on command line: You can run cprofiler on command line as - 
####        $ python -m cProfile particle_benchmark.py
####    use -s tottime to sort by total time 
####    to save output provide -o prof.out to save the output. -o is positional parameter use it after cProfile as - 
####        $ python -m cProfile -o output/particle_benchmark_cprofiler.out -s tottime particle_benchmark.py 
####
####    The output created cannot be read by QCachegrind directly. You need to convert the .out file from cProfiler 
####    to readable format for QCachegrind. 
####    
####    For this execute command - 
####        $ pip install pyprof2calltree
####        $ pyprof2calltree -i output/particle_benchmark_cprofiler.out -o output/particle_benchmark_cprofiler.calltree
####
#### 2. You can also create a program (like this one) to run cprofiler 
####    You can also wrap the profiler around the code. Like particle_cprofiler_wrapped.py 


"""
Output from of $ python -m cProfile -s tottime particle_benchmark.py 

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    2.327    2.327    2.327    2.327 particle.py:30(evolve)
    34/32    0.062    0.002    0.086    0.003 {built-in method _imp.create_dynamic}
      292    0.059    0.000    0.059    0.000 {built-in method _io.open_code}
     7554    0.039    0.000    0.070    0.000 inspect.py:891(cleandoc)
      292    0.033    0.000    0.033    0.000 {built-in method marshal.loads}

ncalls - Number of times function was called
tottime - total time spent by the function without taking inot the account to other functions 
cumtime - time spent by function include other function calls 
percall - time spent for single call of the function - this can be obtained by dividing the total or cummulative time by number of calls 
filename:lineno - filename and line number. this information will not be avaible when calling C extension modules

We can see most time is spent in running evolve function. But does not tell which specific line is causing the bottleneck
We can use line_profiler in such case 

"""

from particle_benchmark import benchmark
import cProfile

cProfile.run("benchmark()")