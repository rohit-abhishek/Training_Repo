""" 
To run the cProfile we will create a new file called exercise_7_cprofile.py which will include run command 
for the cProfiler. 
To perform memory profiling we will comment off @profile command and put @mprofile decorator
and use mprof run Exercise_7 
"""


from Particle_Simulation.particle_tuned_python import Particle, ParticleSimulator
from random import uniform

# added by RA 
from line_profiler import profile
from memory_profiler import profile as mprofile

# @profile
@mprofile
def close(particles, eps=1e-5):
    """ check if two particles are close to each other by less than 1e-5 """
    p0, p1 = particles

    x_dist = abs(p0.x - p1.x)
    y_dist = abs(p0.y - p1.y)

    return x_dist < eps and y_dist < eps

# @profile
@mprofile
def benchmark():
    particles = [
        Particle(uniform(-1.0, 1.0), uniform(-1.0, 1.0), uniform(-1.0, 1.0))
        for i in range(2)
    ]

    simulator = ParticleSimulator(particles)
    simulator.evolve_faster(0.1)

    print(close(particles))


if __name__ == '__main__':
    benchmark()
