""" 
This is 14th program in the series. similar to particle_memory_profiling.py however using particle_tuned_python_memory file classes 
within to generate memeory profile. 

To tun the command use 
    $ mprof run particle_memory_profiling.py

After running this command we can see 112MB size is reduced to 109 MB

Output 

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    13     93.2 MiB     93.2 MiB           1   @profile
    14                                         def benchmark_memory():
    15                                             ''' measure performance '''ß
    16                                         
    17                                             # Generate 1000 particiles with random value between 
    18    109.1 MiB      0.0 MiB           2       particles = [
    19    109.1 MiB      6.7 MiB      200000           Particle(random.uniform(-1.0, 1.0), 
    20    109.1 MiB      9.2 MiB      100000                    random.uniform(-1.0, 1.0), 
    21    109.1 MiB      0.0 MiB      200002                    random.uniform(-1.0, 1.0)) for i in range(100000)
    22                                             ]
    23                                         
    24                                             # create simulartor object and pass all particles 
    25    109.1 MiB      0.0 MiB           1       simulator = ParticleSimulator(particles)
    26    109.1 MiB      0.0 MiB           1       simulator.evolve_faster(0.001)

"""

from particle_tuned_python_memory import Particle, ParticleSimulator
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