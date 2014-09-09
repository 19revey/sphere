#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 18, 'font.family': 'serif'})
import shutil

import os
import numpy
import sphere
from permeabilitycalculator import *
import matplotlib.pyplot as plt

#sigma0_list = numpy.array([1.0e3, 2.0e3, 4.0e3, 10.0e3, 20.0e3, 40.0e3])
sigma0 = 10.0e3
cvals = [1.0, 0.1]
c_phi = 1.0

shear_strain = [[], [], []]
friction = [[], [], []]
dilation = [[], [], []]
p_min = [[], [], []]
p_mean = [[], [], []]
p_max = [[], [], []]

fluid=True

# dry shear
sid = 'shear-sigma0=' + str(10.0e3)
sim = sphere.sim(sid)
sim.readlast()
sim.visualize('shear')
shear_strain[0] = sim.shear_strain
friction[0] = sim.tau/sim.sigma_eff
dilation[0] = sim.dilation

# wet shear
c = 1
for c in numpy.arange(1,len(cvals)+1):
    c_grad_p = cvals[c-1]

    sid = 'shear-sigma0=' + str(sigma0) + '-c_phi=' + \
                    str(c_phi) + '-c_grad_p=' + str(c_grad_p) + \
                    '-hi_mu-lo_visc'
    if os.path.isfile('../output/' + sid + '.status.dat'):

        sim = sphere.sim(sid, fluid=fluid)
        shear_strain[c] = numpy.zeros(sim.status())
        friction[c] = numpy.zeros_like(shear_strain[c])
        dilation[c] = numpy.zeros_like(shear_strain[c])

        sim.readlast()
        sim.visualize('shear')
        shear_strain[c] = sim.shear_strain
        friction[c] = sim.tau/sim.sigma_eff
        dilation[c] = sim.dilation

        # fluid pressures
        p_mean[c] = numpy.zeros_like(shear_strain[c])
        p_min[c] = numpy.zeros_like(shear_strain[c])
        p_max[c] = numpy.zeros_like(shear_strain[c])
        for i in numpy.arange(sim.status()):
            iz_top = int(sim.w_x[0]/(sim.L[2]/sim.num[2]))-1
            p_mean[c][i] = numpy.mean(sim.p_f[:,:,0:iz_top])
            p_min[c][i] = numpy.min(sim.p_f[:,:,0:iz_top])
            p_max[c][i] = numpy.min(sim.p_f[:,:,0:iz_top])

    else:
        print(sid + ' not found')

    # produce VTK files
    #for sid in sids:
        #sim = sphere.sim(sid, fluid=True)
        #sim.writeVTKall()
    c += 1


#fig = plt.figure(figsize=(8,8)) # (w,h)
fig = plt.figure(figsize=(8,12))

#plt.subplot(3,1,1)
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

ax1 = plt.subplot(311)
ax2 = plt.subplot(312, sharex=ax1)
ax3 = plt.subplot(313, sharex=ax1)
ax1.plot(shear_strain[0], friction[0], label='dry')
ax2.plot(shear_strain[0], dilation[0], label='dry')

color = ['b','g','r']
for c in numpy.arange(1,len(cvals)+1):

    ax1.plot(shear_strain[c][1:], friction[c][1:], \
            label='$c$ = %.2f' % (cvals[c-1]))

    ax2.plot(shear_strain[c][1:], dilation[c][1:], \
            label='$c$ = %.2f' % (cvals[c-1]))

    ax3.plot(shear_strain[c][1:], p_max[c][1:], '--' + color[c])
    ax3.plot(shear_strain[c][1:], p_mean[c][1:], '-' + color[c], \
            label='$c$ = %.2f' % (cvals[c-1]))
    ax3.plot(shear_strain[c][1:], p_min[c][1:], '--' + color[c])

ax3.set_xlabel('Shear strain $\\gamma$ [-]')

ax1.set_ylabel('Shear friction $\\tau/\\sigma\'$ [-]')
ax2.set_ylabel('Dilation $\\Delta h/(2r)$ [-]')
ax3.set_ylabel('Fluid pressure $p_f$ [Pa]')

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)

ax1.grid()
ax2.grid()
ax3.grid()

ax1.legend(loc='lower right', prop={'size':18})
ax2.legend(loc='lower right', prop={'size':18})
ax3.legend(loc='lower right', prop={'size':18})

plt.tight_layout()
filename = 'shear-10kPa-stress-dilation.pdf'
#print(os.getcwd() + '/' + filename)
plt.savefig(filename)
shutil.copyfile(filename, '/home/adc/articles/own/2-org/' + filename)
print(filename)
