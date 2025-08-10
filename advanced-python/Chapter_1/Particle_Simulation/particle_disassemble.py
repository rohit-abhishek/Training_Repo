""" 
This is 11th program in the series 
this will disassemble all the instructions of python into equivalent C instructions. 
""" 

import dis 
from particle import Particle, ParticleSimulator

dis.dis(ParticleSimulator.evolve)