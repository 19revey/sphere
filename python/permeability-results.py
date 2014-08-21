#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 18, 'font.family': 'serif'})
import os

import numpy
import sphere
from permeabilitycalculator import *
import matplotlib.pyplot as plt

sids = [
    'permeability-dp=1000.0-c_phi=1.0-c_grad_p=0.01',
    'permeability-dp=1000.0-c_phi=1.0-c_grad_p=0.5',
    'permeability-dp=1000.0',
    'permeability-dp=20000.0-c_phi=1.0-c_grad_p=0.01',
    'permeability-dp=20000.0-c_phi=1.0-c_grad_p=0.1',
    'permeability-dp=20000.0-c_phi=1.0-c_grad_p=0.5',
    'permeability-dp=4000.0-c_phi=1.0-c_grad_p=0.01',
    'permeability-dp=4000.0-c_phi=1.0-c_grad_p=0.1',
    'permeability-dp=4000.0-c_phi=1.0-c_grad_p=0.5',
    'permeability-dp=4000.0']

K = numpy.empty(len(sids))
c_grad_p = numpy.empty_like(K)
i = 0

for sid in sids:
    pc = PermeabilityCalc(sid, plot_evolution=False, print_results=False,
            verbose=False)
    K[i] = pc.conductivity()
    c_grad_p[i] = pc.c_grad_p()
    i += 1
        

# produce VTK files
#for sid in sids:
    #sim = sphere.sim(sid, fluid=True)
    #sim.writeVTKall()

fig = plt.figure()
plt.xlabel('Pressure gradient coefficient $c$ [-]')
plt.ylabel('Hydraulic conductivity $K$ [m/s]')
plt.plot(c_grad_p, K, '+')
plt.grid()
plt.tight_layout()
filename = 'c_grad_p-vs-K.pdf'
plt.savefig(filename)
print(os.getcwd() + '/' + filename)
