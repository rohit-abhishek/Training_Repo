### This is second program to measure the running time of applicaiton. 
### Benchmark is useful to keep score of how fast program is with new version that we implement 
### run the program using command - 
###         time python particle_benchmark.py
### unix time comamnd is powerful and provide a very simple way to benchmark the program. Spits out result as - 
###         real: Actual time spent to run the program from start to finish. As if there is a stopwatch 
###.        user: cummulative time spent by all CPU during the computations
###.        sys: cummulative time spent by all CPU during system related tasks
######################################################################################################################################

from particle import Particle, ParticleSimulator
import random



def benchmark(): 
    """ measure performance """

    # Generate 1000 particiles with random value between 
    particles = [
        Particle(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)) for i in range(1000)
    ]

    # create simulartor object and pass all particles 
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)

if __name__ == "__main__":
    benchmark()