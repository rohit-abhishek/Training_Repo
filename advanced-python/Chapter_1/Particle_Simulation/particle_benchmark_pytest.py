### This is 6th code for testing the particle simulator application. 

### The code is for unit testing the particle. simulate them for 0.1 time units and compare those with reference implementation 
### since the function used in particle file is evolve() method; we will use test_evolve method for this 
### This ensures correctness of our functionality but tells very little about the running time. 
### Run this program using pytest on command line as - 
###             $ pytest particle_benchmark_pytest.py::test_evolve

""" 
output of this program will be 
particle_benchmark_pytest.py .                                                                                                                                                      [100%]

-------------------------------------------- benchmark: 1 tests --------------------------------------------
Name (time in ms)        Min     Max    Mean  StdDev  Median     IQR  Outliers       OPS  Rounds  Iterations
------------------------------------------------------------------------------------------------------------
test_evolve           7.0543  7.4748  7.1854  0.0691  7.1752  0.0846      38;2  139.1701     140           1
------------------------------------------------------------------------------------------------------------

Here test_evolve was executed 140 times. Min and Max are timings ranging between 7.0543 and 7.4648 ms 

"""

from particle import Particle, ParticleSimulator

def test_evolve(benchmark):
    """ Testing particle similuator. Pass benchmark as parameter to method you want to check the performance of """

    # create particles at different position and angular velocity 
    particles = [
        Particle(0.3, 0.5, +1), 
        Particle(0.0, -0.5, -1), 
        Particle(-0.1, -0.4, 3)
    ]

    # create simulator objects for all particles 
    simulator = ParticleSimulator(particles)
    simulator.evolve(0.1)

    # take each particle separately
    p0, p1, p2 = particles

    # define a sub funciton to return boolean value for particle position 
    def fequal(a, b, eps=1e-5):
        return abs(a-b) < eps 
    
    # All conditions below will be met therefore no error will be returned 
    assert fequal(p0.x, 0.210269)
    assert fequal(p0.y, 0.543863)

    assert fequal(p1.x, -0.099334)
    assert fequal(p1.y, -0.490034)

    assert fequal(p2.x, 0.191358)
    assert fequal(p2.y, -0.365227)

    benchmark(simulator.evolve, 0.1)


if __name__ == "__main__":
    test_evolve()