#!/usr/bin/env python

# Import sphere functionality
from sphere import *

### EXPERIMENT SETUP ###
initialization = True
consolidation  = True
shearing       = True
rendering      = True
plots          = True

# Number of particles
np = 1e4

# Common simulation id
sim_id = "shear-test-devs3"

# Deviatoric stress [Pa]
devslist = [80e3, 10e3, 20e3, 40e3, 60e3, 120e3]
#devs = 0

### INITIALIZATION ###

# New class
init = Spherebin(np = np, nd = 3, nw = 0, sid = sim_id + "-init")

# Save radii
init.generateRadii(radius_mean = 0.02)

# Use default params
init.defaultParams(gamma_n = 100.0, mu_s = 0.6, mu_d = 0.6)

# Add gravity
init.g[2] = -9.81

# Initialize positions in random grid (also sets world size)
hcells = np**(1.0/3.0)
init.initRandomGridPos(gridnum = numpy.array([hcells, hcells, 1e9]), periodic = 1, contactmodel = 2)

# Set duration of simulation
init.initTemporal(total = 5.0)

if (initialization == True):

    # Run sphere
    init.run(dry = True)
    init.run()

    if (plots == True):
        # Make a graph of energies
        visualize(init.sid, "energy", savefig=True, outformat='png')

    init.writeVTKall()

    if (rendering == True):
        # Render images with raytracer
        init.render(method = "angvel", max_val = 0.3, verbose = False)



# For each normal stress, consolidate and subsequently shear the material
for devs in devslist:

    ### CONSOLIDATION ###

    # New class
    cons = Spherebin(np = init.np, nw = 1, sid = sim_id + "-cons-devs{}".format(devs))

    # Read last output file of initialization step
    lastf = status(sim_id + "-init")
    cons.readbin("../output/" + sim_id + "-init.output{:0=5}.bin".format(lastf), verbose=False)

    # Setup consolidation experiment
    cons.consolidate(deviatoric_stress = devs, periodic = init.periodic)


    # Set duration of simulation
    cons.initTemporal(total = 1.5)
    #cons.initTemporal(total = 0.0019, file_dt = 0.00009)
    #cons.initTemporal(total = 0.0019, file_dt = 1e-6)
    #cons.initTemporal(total = 0.19, file_dt = 0.019)

    """
    cons.w_m[0] *= 0.001
    cons.mu_s[0] = 0.0
    cons.mu_d[0] = 0.0
    cons.gamma_wn[0] = 1e4
    cons.gamma_wt[0] = 1e4
    cons.contactmodel[0] = 1
    """

    if (consolidation == True):

        # Run sphere
        cons.run(dry = True) # show values, don't run
        cons.run() # run

        if (plots == True):
            # Make a graph of energies
            visualize(cons.sid, "energy", savefig=True, outformat='png')
            visualize(cons.sid, "walls", savefig=True, outformat='png')

        cons.writeVTKall()

        if (rendering == True):
            # Render images with raytracer
            cons.render(method = "pres", max_val = 2.0*devs, verbose = False)


    ### SHEARING ###

    # New class
    shear = Spherebin(np = cons.np, nw = cons.nw, sid = sim_id + "-shear-devs{}".format(devs))

    # Read last output file of initialization step
    lastf = status(sim_id + "-cons-devs{}".format(devs))
    shear.readbin("../output/" + sim_id + "-cons-devs{}.output{:0=5}.bin".format(devs, lastf), verbose = False)

    # Setup shear experiment
    shear.shear(shear_strain_rate = 0.05, periodic = init.periodic)

    # Set duration of simulation
    shear.initTemporal(total = 20.0)

    if (shearing == True):

        # Run sphere
        shear.run(dry = True)
        shear.run()

        if (plots == True):
            # Make a graph of energies
            visualize(shear.sid, "energy", savefig=True, outformat='png')
            visualize(shear.sid, "shear", savefig=True, outformat='png')

        shear.writeVTKall()

        if (rendering == True):
            # Render images with raytracer
            shear.render(method = "pres", max_val = 2.0*devs, verbose = False)
