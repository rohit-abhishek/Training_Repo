""" 
This is 12th program in the series 

We will use memory profiler to find the overhead due to creation of multiple particles

memory_profiler just like line_profiler requires instrumentation of source code by placing a @profile decorator function 

Only difference is in line_profile profile decorator needed no explicit import due to kernprof command utilizing the namespace 
However, memory_profiler needs to be inlcuded in the import statement 

To tun the command use 
    $ mprof run particle_memory_profiling.py

This will create outputfile with extension .dat with memory trace 

The output - 
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    16     92.7 MiB     92.7 MiB           1   @profile
    17                                         def benchmark_memory():
    18                                             ''' measure performance '''
    19                                         
    20                                             # Generate 1000 particiles with random value between 
    21    112.0 MiB      0.0 MiB           2       particles = [
    22    112.0 MiB     19.2 MiB      100002           Particle(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for i in range(100000)
    23                                             ]
    24                                         
    25                                             # create simulartor object and pass all particles 
    26    112.0 MiB      0.0 MiB           1       simulator = ParticleSimulator(particles)
    27    112.0 MiB      0.0 MiB           1       simulator.evolve_faster(0.001)

We can use slots in the particle_tuned_python.py program to reduce memory footprint 

""" 

from particle_tuned_python import Particle, ParticleSimulator
import psutil, random
from memory_profiler import profile

@profile
def benchmark_memory():
    """ measure performance """

    # Generate 1000 particiles with random value between 
    particles = [
        Particle(random.uniform(-1.0, 1.0), 
                 random.uniform(-1.0, 1.0), 
                 random.uniform(-1.0, 1.0)) for i in range(100000)
    ]

    # create simulartor object and pass all particles 
    simulator = ParticleSimulator(particles)
    simulator.evolve_faster(0.001)

if __name__ == "__main__":
    benchmark_memory()