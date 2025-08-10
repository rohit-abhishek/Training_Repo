from Exercise_7 import benchmark
import cProfile 

pr = cProfile.Profile() 
pr.enable() 
benchmark()
pr.disable()
pr.print_stats()
