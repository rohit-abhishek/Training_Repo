#### This is 8th code in the whole series 

#### See program particle_cprofiler.py which has 2 ways of calling cprofiler 

import cProfile
from particle_benchmark import benchmark

pr = cProfile.Profile() 
pr.enable() 
benchmark()
pr.disable()
pr.print_stats()

""" 
We can see most time is spent in evolve funciton. But does not tell which specific line is causing the bottleneck. 
We can use line_profiler in such case 

"""