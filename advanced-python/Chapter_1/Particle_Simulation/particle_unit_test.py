### This is first code for testing the particle simulator application. 

### The code is for unit testing the particle. simulate them for 0.1 time units and compare those with reference implementation 
### since the function used in particle file is evolve() method; we will use test_evolve method for this 
### This ensures correctness of our functionality but tells very little about the running time. 
### Run this program on VS code 

from particle import Particle, ParticleSimulator

def test_evolve():
    """ Testing particle similuator """

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

    # Below condition will fail 
    assert fequal(p0.x, 0.010269)
    assert fequal(p0.y, 0.243863)

if __name__ == "__main__":
    test_evolve()