#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams.update({'font.size': 7, 'font.family': 'sans-serif'})
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
import shutil

import os
import sys
import numpy
import sphere
import matplotlib.pyplot as plt
import matplotlib.patches

sid = 'halfshear-darcy-sigma0=80000.0-k_c=3.5e-13-mu=1.04e-07-ss=10000.0-A=70000.0-f=0.2'
outformat = 'pdf'
fluid = True
#threshold = 100.0 # [N]
calculateforcechains = False
legend_alpha=0.5


###################
#### DATA READ ####
###################

sim = sphere.sim(sid, fluid=fluid)
sim.readfirst()

#nsteps = 2
#nsteps = 10
#nsteps = 400
nsteps = sim.status()

t = numpy.empty(nsteps)

# Stress plot
sigma_def = numpy.empty_like(t)
sigma_eff = numpy.empty_like(t)
tau_def   = numpy.empty_like(t)
tau_eff   = numpy.empty_like(t)
p_f_bar   = numpy.empty_like(t)
p_f_top   = numpy.empty_like(t)

# shear velocity plot
v         = numpy.empty_like(t)

# displacement and mean porosity plot
xdisp     = numpy.empty_like(t)
phi_bar   = numpy.empty_like(t)

# mean horizontal porosity plot
poros     = numpy.empty((sim.num[2], nsteps))
zpos_c    = numpy.empty(sim.num[2])
dz = sim.L[2]/sim.num[2]
for i in numpy.arange(sim.num[2]):
    zpos_c[i] = i*dz + 0.5*dz

# Contact statistics plot
n                  = numpy.empty(nsteps)
coordinationnumber = numpy.empty(nsteps)
nkept              = numpy.empty(nsteps)


for i in numpy.arange(nsteps):

    sim.readstep(i+1)

    t[i]         = sim.currentTime()

    sigma_def[i] = sim.currentNormalStress('defined')
    sigma_eff[i] = sim.currentNormalStress('effective')
    tau_def[i]   = sim.shearStress('defined')
    tau_eff[i]   = sim.shearStress('effective')

    phi_bar[i]   = numpy.mean(sim.phi[:,:,0:sim.wall0iz()])
    p_f_bar[i]   = numpy.mean(sim.p_f[:,:,0:sim.wall0iz()])
    p_f_top[i]   = sim.p_f[0,0,-1]

    v[i]         = sim.shearVelocity()
    xdisp[i]     = sim.shearDisplacement()

    poros[:,i]   = numpy.average(numpy.average(sim.phi, axis=0),axis=0)

    if calculateforcechains:
        if i > 0:
            loaded_contacts_prev = numpy.copy(loaded_contacts)
            pairs_prev = numpy.copy(sim.pairs)

        loaded_contacts = sim.findLoadedContacts(
                threshold = sim.currentNormalStress()*2.)
                #sim.currentNormalStress()/1000.)
        n[i] = numpy.size(loaded_contacts)

        sim.findCoordinationNumber()
        coordinationnumber[i] = sim.findMeanCoordinationNumber()

        nfound = 0
        if i > 0:
            for a in loaded_contacts[0]:
                for b in loaded_contacts_prev[0]:
                    if (sim.pairs[:,a] == pairs_prev[:,b]).all():
                        nfound += 1;

        nkept[i] = nfound

        print coordinationnumber[i]
        print nfound


if calculateforcechains:
    numpy.savetxt(sid + '-fc.txt', (n, nkept, coordinationnumber))
else:
    n, nkept, coordinationnumber = numpy.loadtxt(sid + '-fc.txt')




##################
#### PLOTTING ####
##################
bbox_x = 0.03
bbox_y = 0.96
verticalalignment='top'
horizontalalignment='left'
fontweight='bold'
bbox={'facecolor':'white', 'alpha':1.0, 'pad':3}

fig = plt.figure(figsize=[3.5,8])

## ax1: N, tau, ax2: p_f
ax1 = plt.subplot(5, 1, 1)
lns0 = ax1.plot(t, sigma_def/1000., '-k', label="$\\sigma_0$")
#lns1 = ax1.plot(t, sigma_eff/1000., '-k', label="$\\sigma'$")
#lns2 = ax1.plot(t, tau_def/1000., '-r', label="$\\tau$")
#ns2 = ax1.plot(t, tau_def/1000., '-r')
lns3 = ax1.plot(t, tau_eff/1000., '-r', label="$\\tau'$")

ax1.set_ylabel('Stress [kPa]')
ax2 = ax1.twinx()
ax2color = 'blue'
#lns4 = ax2.plot(t, p_f_top/1000.0 + 80.0, '-',
        #color=ax2color,
        #label='$p_\\text{f}^\\text{forcing}$')
lns5 = ax2.plot(t, p_f_bar/1000.0 + 80.0, '--',
        color=ax2color,
        label='$\\bar{p}_\\text{f}$')
ax2.set_ylabel('Mean fluid pressure [kPa]')
ax2.yaxis.label.set_color(ax2color)
for tl in ax2.get_yticklabels():
    tl.set_color(ax2color)
    #ax2.legend(loc='upper right')
#lns = lns0+lns1+lns2+lns3+lns4+lns5
#lns = lns0+lns1+lns2+lns3+lns5
#lns = lns1+lns3+lns5
lns = lns0+lns3+lns5
labs = [l.get_label() for l in lns]
ax2.legend(lns, labs, loc='upper right', ncol=3,
        fancybox=True, framealpha=legend_alpha)
ax1.set_ylim([-30, 200])
ax2.set_ylim(ax1.get_ylim())

ax1.text(bbox_x, bbox_y, 'a',
        horizontalalignment=horizontalalignment,
        verticalalignment=verticalalignment,
        fontweight=fontweight, bbox=bbox,
        transform=ax1.transAxes)


## ax3: v, ax4: unused
ax3 = plt.subplot(5, 1, 2, sharex=ax1)
ax3.semilogy(t, v, 'k')
ax3.set_ylabel('Shear velocity [ms$^{-1}$]')
# shade stick periods
collection = matplotlib.collections.BrokenBarHCollection.span_where(
                t, ymin=1.0e-11, ymax=1.0,
                where=numpy.isclose(v, 0.0),
                facecolor='black', alpha=0.2,
                linewidth=0)
ax3.add_collection(collection)

ax3.text(bbox_x, bbox_y, 'b',
        horizontalalignment=horizontalalignment,
        verticalalignment=verticalalignment,
        fontweight=fontweight, bbox=bbox,
        transform=ax3.transAxes)


## ax5: xdisp, ax6: mean(phi)
ax5 = plt.subplot(5, 1, 3, sharex=ax1)
ax5.plot(t, xdisp, 'k')
ax5.set_ylabel('Shear displacement [m]')

ax6color='blue'
ax6 = ax5.twinx()
ax6.plot(t, phi_bar, color=ax6color)
ax6.set_ylabel('Mean porosity [-]')
ax6.yaxis.label.set_color(ax6color)
for tl in ax6.get_yticklabels():
    tl.set_color(ax6color)

ax6.text(bbox_x, bbox_y, 'c',
        horizontalalignment=horizontalalignment,
        verticalalignment=verticalalignment,
        fontweight=fontweight, bbox=bbox,
        transform=ax6.transAxes)


## ax7: n_heavy, dn_heavy, ax8: z
ax7 = plt.subplot(5, 1, 4, sharex=ax1)
ax7.semilogy(t, n, 'k', label='$n_\\text{heavy}$')
ax7.set_ylabel('Number of heavily loaded contacts [-]')
#ax7.semilogy(t, n - nkept, 'b', label='$\Delta n_\\text{heavy}$')
ax7.set_ylim([1.0e1, 2.0e4])

ax8 = ax7.twinx()
ax8color='green'
ax8.plot(t, coordinationnumber, color=ax8color)
ax8.set_ylabel('Coordination number [-]')
ax8.yaxis.label.set_color(ax8color)
for tl in ax8.get_yticklabels():
    tl.set_color(ax8color)
ax8.set_ylim([-0.2,9.8])

ax7.text(bbox_x, bbox_y, 'd',
        horizontalalignment=horizontalalignment,
        verticalalignment=verticalalignment,
        fontweight=fontweight, bbox=bbox,
        transform=ax7.transAxes)


## ax9: porosity, ax10: unused
ax9 = plt.subplot(5, 1, 5, sharex=ax1)
#poros_max = numpy.max(poros[0:sim.wall0iz(),:])
#poros_min = numpy.min(poros)
#poros_max = 0.44
poros_max = 0.45
poros_min = 0.37
cmap = matplotlib.cm.get_cmap('Blues_r')
im9 = ax9.pcolormesh(t, zpos_c, poros,
        cmap=cmap,
        #cmap=matplotlib.cm.get_cmap('bwr'),
        #cmap=matplotlib.cm.get_cmap('coolwarm'),
        #vmin=-p_ext, vmax=p_ext,
        vmin=poros_min, vmax=poros_max,
        rasterized=True)
ax9.set_ylim([zpos_c[0], sim.w_x[0]])
ax9.set_ylabel('Vertical position [m]')
#cb9 = plt.colorbar(im9, orientation='horizontal')#, pad=0.20)
cbaxes = fig.add_axes([0.32, 0.1, 0.4, 0.01]) # x,y,w,h
#cb9 = plt.colorbar(im9, orientation='horizontal', shrink=0.7)
#ax9.add_patch(matplotlib.patches.Rectangle(
    #(3.0, 0.06), # x,y
    #15., # dx
    #.15, # dy
    #fill=True,
    #linewidth=1,
    #facecolor='white'))
ax9.add_patch(matplotlib.patches.Rectangle(
    (3.0, 0.04), # x,y
    15., # dx
    .15, # dy
    fill=True,
    linewidth=1,
    facecolor='white'))

cb9 = plt.colorbar(im9, cax=cbaxes,
        ticks=[poros_min, poros_min + 0.5*(poros_max-poros_min), poros_max],
        orientation='horizontal',
        extend='min', cmap=cmap)
cmap.set_under([8./255., 48./255., 107./255.])
cb9.set_label('Mean horizontal porosity [-]')
'''
ax9.text(0.5, 0.4, 'Mean horizontal porosity [-]\\\\',
        horizontalalignment='center',
        verticalalignment='center',
        bbox={'facecolor':'white', 'alpha':1.0, 'pad':3})
'''
#cb9.solids.set_rasterized(True)

ax9.text(bbox_x, bbox_y, 'e',
        horizontalalignment=horizontalalignment,
        verticalalignment=verticalalignment,
        fontweight=fontweight, bbox=bbox,
        transform=ax9.transAxes)



plt.setp(ax1.get_xticklabels(), visible=False)
#plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
#plt.setp(ax4.get_xticklabels(), visible=False)
plt.setp(ax5.get_xticklabels(), visible=False)
#plt.setp(ax6.get_xticklabels(), visible=False)
plt.setp(ax7.get_xticklabels(), visible=False)
#plt.setp(ax8.get_xticklabels(), visible=False)

ax9.set_xlabel('Time [s]')
fig.tight_layout()
plt.subplots_adjust(hspace=0.05)

plt.savefig(sid + '-combined.' + outformat)
plt.close()
