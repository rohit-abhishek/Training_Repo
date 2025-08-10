""" 
This is clone of program particle_line_profiler.py. And this is 10th program in this series making use of line_profiler utility. 

After running particle_line_profiler we get a clear idea where exactly program is spending more time. 
This code will deal with tuning the performance. Output created 

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    44                                               @profile
    45                                               def evolve(self, dt, time_step=0.00001): 
    46                                                   ''' calculate the motion of the particle'''
    47       135        129.0      1.0      0.0          n_steps = int(dt/time_step)
    48                                           
    49                                                   # for every timestep calculate the v_x and v_y 
    50    135000      36516.0      0.3      4.0          for i in range(n_steps):
    51    539460     136173.0      0.3     15.0              for p in self.particles:
    52    404595     142795.0      0.4     15.8                  norm = (p.x ** 2 + p.y ** 2) ** 0.5
    53                                           
    54                                                           # unit tangent vectors for x and y direction for uniform circular motion 
    55    404595      96462.0      0.2     10.7                  v_x = -p.y/norm 
    56    404595      94886.0      0.2     10.5                  v_y = p.x/norm
    57                                           
    58                                                           # displacements made by the particle 
    59    404595     100131.0      0.2     11.1                  d_x = time_step * p.ang_vel * v_x 
    60    404595      99987.0      0.2     11.0                  d_y = time_step * p.ang_vel * v_y 
    61                                           
    62                                                           # update the particle position 
    63    404595      98991.0      0.2     10.9                  p.x += d_x 
    64    404595      99277.0      0.2     11.0                  p.y += d_y 


In this case the algorithm needs to change. It would be efficient to express the motion in terms of radius "r" 
angle alpha instead of x and y 
x = r*cos(alpha)
y = r*sin(alpha)

Another is to minimize the number of instruction e.g. precalculate timestep*p.ang_vel factor which will not change with time 

Also simple assignments are taking way too longer. e.g. v_x = -p.y/norm. Reduce the number of assignments

We will create a new method called evolve_faster with the changes and profile it again using 
    $ kernprof -l -v particle_tuned_python.py 
    
The output will be 
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    94                                               @profile 
    95                                               def evolve_faster(self, dt, time_step=0.00001) : 
    96                                                   ''' Evolve faster '''
    97                                           
    98       233        263.0      1.1      0.0          n_steps = int(dt/time_step)
    99                                           
   100                                                   # change the loop order 
   101       932        541.0      0.6      0.1          for p in self.particles:
   102       699        324.0      0.5      0.0              t_x_ang = time_step * p.ang_vel 
   103    699000     193563.0      0.3     28.2              for i in range(n_steps):
   104    698301     254618.0      0.4     37.1                  norm = (p.x**2 + p.y**2)**0.5
   105    698301     236282.0      0.3     34.5                  p.x, p.y = (p.x - t_x_ang * p.y/norm, p.y + t_x_ang * p.x/norm)

   We can see we got modest performance benefit with pure python implementation. 
"""

import matplotlib.pyplot as plt 
import matplotlib as mpl 
from matplotlib import animation

class Particle:
    """ class for creating particles """
    
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