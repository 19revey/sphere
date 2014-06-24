#!/usr/bin/env python
import sphere
from pytestutils import *

sim = sphere.sim('fluid_particle_interaction', fluid=True)
sim.cleanup()

sim.defineWorldBoundaries([1.0, 1.0, 1.0], dx = 0.1)
sim.initFluid()
sim.rho[0] = 1000.0 # particle density = fluid density
sim.setDEMstepsPerCFDstep(100)


# No gravity, pressure gradient enforced by Dirichlet boundaries.
# The particle should be sucked towards the low pressure
print('# Test 1: Test pressure gradient force')
sim.p_f[:,:,0]  = 10.0
sim.p_f[:,:,-1] = 1.0
sim.addParticle([0.5, 0.5, 0.5], 0.05)
sim.initTemporal(total=0.1, file_dt=0.01)

sim.run()
#sim.writeVTKall()

sim.readlast()
test(sim.vel[0,2] > 0.0, 'Particle velocity:')



# Sidewards gravity, homogenous pressure, Neumann boundaries.
# Fluid should flow towards +x and drag particles in the same direction
print('# Test 2: Test fluid drag force')
sim.initFluid()
sim.zeroKinematics()
sim.bc_bot[0] = 2   # no-slip
sim.bc_top[0] = 2   # no-slip
sim.g[0] = 10.0

sim.deleteParticle(0)
sim.addParticle([0.5, 0.5, 0.75], 0.05)
sim.addParticle([0.5, 0.5, 0.50], 0.05)
sim.addParticle([0.5, 0.5, 0.25], 0.05)

sim.initTemporal(total=0.1, file_dt=0.01)

sim.run()
#sim.writeVTKall()

sim.readlast()
test(sim.v_f[:,:,:,0] > 0.0, 'Fluid velocity:')
test(sim.vel[0,0] > 0.0, 'Particle 0 velocity:')
test(sim.vel[1,0] > 0.0, 'Particle 1 velocity:')
test(sim.vel[2,0] > 0.0, 'Particle 2 velocity:')


#sim.cleanup()
