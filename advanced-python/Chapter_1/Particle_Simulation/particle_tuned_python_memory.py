""" 
This is 13th program in the series. This is created as clone of particle_tuned_python.py after running particle_memory_profiling.py

Adding __slots__ will reduce memory footprint for particles. 
This features saves some memory by avoiding storage of variable of instance in an internal dicitionary. 
This strategy has smaller limitation - it prevents the addition of attributes other than specified ones in __slots__

New program particle_memory_profiling_tuned.py is created to create output of memory profile for this program
""" 

import matplotlib.pyplot as plt 
import matplotlib as mpl 
from matplotlib import animation

class Particle:
    """ class for creating particles """

    __slots__ = ('x', 'y', 'ang_vel')
    
    def __init__(self, x, y, ang_vel):
        """ Accepts X, Y and initial angular velocity of particle """
        self.x = x 
        self.y = y 
        self.ang_vel = ang_vel 


class ParticleSimulator: 
    """ Class for Particle Simulator. this will accept all particles which needs simulation """

    def __init__(self, particles):
        self.particles = particles 
    
    # we want particles to rotate at every timestep with center at x = 0 and y = 0 
    # the direction of particle will be always perpendicular to direction of the center 
    # take smaller steps and calculate v_x and v_y i.e. direction of the motion for tiny timestep dt 
    # and d_x and d_y i.e. displacement of the pariticle. 

    # @profile
    # def evolve(self, dt, time_step=0.00001): 
    #     """ calculate the motion of the particle """
    #     n_steps = int(dt/time_step)

    #     # for every timestep calculate the v_x and v_y 
    #     for i in range(n_steps):
    #         for p in self.particles:
    #             norm = (p.x ** 2 + p.y ** 2) ** 0.5

    #             # unit tangent vectors for x and y direction for uniform circular motion 
    #             v_x = -p.y/norm 
    #             v_y = p.x/norm

    #             # displacements made by the particle 
    #             d_x = time_step * p.ang_vel * v_x 
    #             d_y = time_step * p.ang_vel * v_y 

    #             # update the particle position 
    #             p.x += d_x 
    #             p.y += d_y        
    # 


    def evolve_faster(self, dt, time_step=0.00001) : 
        """ Evolve faster """

        n_steps = int(dt/time_step)

        # change the loop order 
        for p in self.particles:
            t_x_ang = time_step * p.ang_vel 
            for i in range(n_steps):
                norm = (p.x**2 + p.y**2)**0.5
                p.x, p.y = (p.x - t_x_ang * p.y/norm, p.y + t_x_ang * p.x/norm)



# use matplotlib animation function to visualize the simulation 
def visualize(simulator):
    """ Visualize the particles """

    # get starting x and y cordinates for particles 
    x = [p.x for p in simulator.particles]
    y = [p.y for p in simulator.particles]

    # create matplot lib figure 
    fig = plt.figure() 
    ax = plt.subplot(111, aspect="equal")
    (line,) = ax.plot(x,y,"bo")

    
    # limit the axes so that 0, 0 is at the center 
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)

    # run the animation 
    def init(): 
        line.set_data([], [])
        return (line, )

    def animate(i):
        simulator.evolve_faster(0.01)
        x = [p.x for p in simulator.particles]
        y = [p.y for p in simulator.particles]

        line.set_data(x, y)

        return (line, )
    
    # call animate function 
    anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True, interval=10)

    # show the graph 
    plt.show()


# create function to create particle and call particle simulator object 
def test_visualize():
    particles = [
        Particle(0.3, 0.5, 1), 
        Particle(0.0, 0.5, -1),
        Particle(-0.1, -0.4, 2)
    ]
    simulator = ParticleSimulator(particles)

    # call visualize 
    visualize(simulator)


# entry of the program 
if __name__ == "__main__": 
    test_visualize()