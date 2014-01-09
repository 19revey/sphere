#!/usr/bin/env python
from pytestutils import *

import sphere
from sphere import visualize, status
import sys
import numpy

print("### CFD tests ###")

# Iteration and conservation of mass test
orig = sphere.Spherebin(np = 1e4, nd = 3, nw = 0, sid = "cfdtest", fluid = True)
orig.generateRadii(radius_mean = 0.05, histogram=False)
orig.defaultParams(mu_s = 0.4, mu_d = 0.4, nu = 8.9e-4)
orig.initRandomGridPos(gridnum = numpy.array([40, 40, 1000]), periodic = 1, contactmodel = 1)
#orig.initTemporal(total = 0.002, file_dt = 0.001)
orig.initTemporal(total = 0.02, file_dt = 0.001)
orig.initFluid(nu = 8.9e-4)
orig.g[2] = 0.0
orig.writebin(verbose=False)
#orig.run(verbose=False)
orig.run()
orig.writeVTKall()
py = Spherebin(sid = orig.sid, fluid = True)
ones = numpy.ones((orig.num))
py.readlast(verbose=False)
compareNumpyArrays(ones, py.p_f, "Fluid pressure conservation:")

# Convergence rate
it = numpy.loadtxt("../output/" + orig.sid + "-conv.log")
compare(it[:,1].sum(), 0.0, "Convergence rate:\t")

