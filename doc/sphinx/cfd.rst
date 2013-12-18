Fluid simulation by CFD
=======================
Following the outline presented by `Limache and Idelsohn (2006)`_, the
continuity equation for an incompressible fluid material is given by:

.. math::
    \nabla \cdot \boldsymbol{v} = 0

and the momentum equation:

.. math::
    \rho \frac{\partial \boldsymbol{v}}{\partial t}
    + \rho (\boldsymbol{v} \cdot \nabla \boldsymbol{v})
    = \nabla \cdot \boldsymbol{\sigma}
    + \rho \boldsymbol{f}_g

Here, :math:`\boldsymbol{v}` is the fluid velocity, :math:`\rho` is the
fluid density, :math:`\boldsymbol{\sigma}` is the `Cauchy stress tensor`_, and
:math:`\boldsymbol{f}_g` is the gravitational force. For incompressible
Newtonian fluids, the Cauchy stress is given by:

.. math::
    \boldsymbol{\sigma} = -p \boldsymbol{I} + \boldsymbol{\tau}

:math:`p` is the fluid pressure, :math:`\boldsymbol{I}` is the identity
tensor, and :math:`\boldsymbol{\tau}` is the deviatoric stress tensor, given
by:

.. math::
    \boldsymbol{\tau} =
    \nu \nabla \boldsymbol{v}
    + \nu (\nabla \boldsymbol{v})^T

By using the following vector identities:

.. math::
    \nabla \cdot (p \boldsymbol{I}) = \nabla p

    \nabla \cdot (\nabla \boldsymbol{v}) = \nabla^2 \boldsymbol{v}

    \nabla \cdot (\nabla \boldsymbol{v})^T
    = \nabla (\nabla \cdot \boldsymbol{v})

the deviatoric component of the Cauchy stress tensor simplifies to the
following, assuming that spatial variations in the viscosity can be neglected:

.. math::
    = -\nabla p
    + \nu \nabla^2 \boldsymbol{v}

The porosity value (in the saturated porous medium the volumetric fraction of
the fluid phase) denoted :math:`\phi` is incorporated in the continuity and
momentum equations. The continuity equation becomes:

.. math::
    \frac{\partial \phi}{\partial t}
    + \nabla \cdot (\phi \boldsymbol{v}) = 0

For the :math:`x` component, the Lagrangian formulation of the momentum equation
with a body force :math:`\boldsymbol{g}` becomes:

.. math::
    \frac{D (\phi v_x)}{D t}
    = \frac{1}{\rho} \left[ \nabla \cdot (\phi \boldsymbol{\sigma}) \right]_x
    + \phi g_x

In the Eulerian formulation, an advection term is added, and the Cauchy stress
tensor is represented as isotropic and deviatoric components individually:

.. math::
    \frac{\partial (\phi v_x)}{\partial t}
    + \boldsymbol{v} \cdot \nabla (\phi v_x)
    = \frac{1}{\rho} \left[ \nabla \cdot (-\phi p \boldsymbol{I})
    + \phi \boldsymbol{\tau}) \right]_x
    + \phi g_x

Using vector identities to rewrite the advection term, and expanding the fluid
stress tensor term:

.. math::
    \frac{\partial (\phi v_x)}{\partial t}
    + \nabla \cdot (\phi v_x \boldsymbol{v})
    - \phi v_x (\nabla \cdot \boldsymbol{v})
    = \frac{1}{\rho} \left[ -\nabla \phi p \right]_x
    + \frac{1}{\rho} \left[ -\phi \nabla p \right]_x
    + \frac{1}{\rho} \left[ \nabla \cdot (\phi \boldsymbol{\tau}) \right]_x
    + \phi g_x

Spatial variations in the porosity are neglected:

.. math::
    \nabla \phi := 0

and the pressure is attributed to the fluid phase alone (model B in Zhu et al.
2007 and Zhou et al. 2010). The divergence of fluid velocities is defined to be
zero:

.. math::
    \nabla \cdot \boldsymbol{v} := 0

With these assumptions, the momentum equation simplifies to:

.. math::
    \frac{\partial (\phi v_x)}{\partial t}
    + \nabla \cdot (\phi v_x \boldsymbol{v})
    = -\frac{1}{\rho} \frac{\partial p}{\partial x}
    + \frac{1}{\rho} \left[ \nabla \cdot (\phi \boldsymbol{\tau}) \right]_x
    + \phi g_x

The remaining part of the advection equation is for the :math:`x` component
found as:

.. math::
    \nabla \cdot (\phi v_x \boldsymbol{v}) =
    \left[
        \frac{\partial}{\partial x},
        \frac{\partial}{\partial y},
        \frac{\partial}{\partial z}
    \right]
    \left[
        \begin{array}{c}
            \phi v_x v_x\\
            \phi v_x v_y\\
            \phi v_x v_z\\
        \end{array}
    \right]
    =
    \frac{\partial (\phi v_x v_x)}{\partial x} +
    \frac{\partial (\phi v_x v_y)}{\partial y} +
    \frac{\partial (\phi v_x v_z)}{\partial z}

The deviatoric stress tensor is in this case symmetrical, i.e. :math:`\tau_{ij}
= \tau_{ji}`, and is found by:

.. math::
    \frac{1}{\rho} \left[ \nabla \cdot (\phi \boldsymbol{\tau}) \right]_x
    = \frac{1}{\rho}
    \left[
        \left[
            \frac{\partial}{\partial x},
            \frac{\partial}{\partial y},
            \frac{\partial}{\partial z}
        \right]
        \phi
        \left[
            \begin{matrix}
                \tau_{xx} & \tau_{xy} & \tau_{xz}\\
                \tau_{yx} & \tau_{yy} & \tau_{yz}\\
                \tau_{zx} & \tau_{zy} & \tau_{zz}\\
            \end{matrix}
        \right]
    \right]_x

    = \frac{1}{\rho}
    \left[
        \begin{array}{c}
            \frac{\partial (\phi \tau_{xx})}{\partial x}
            + \frac{\partial (\phi \tau_{xy})}{\partial y}
            + \frac{\partial (\phi \tau_{xz})}{\partial z}\\
            \frac{\partial (\phi \tau_{yx})}{\partial x}
            + \frac{\partial (\phi \tau_{yy})}{\partial y}
            + \frac{\partial (\phi \tau_{yz})}{\partial z}\\
            \frac{\partial (\phi \tau_{zx})}{\partial x}
            + \frac{\partial (\phi \tau_{zy})}{\partial y}
            + \frac{\partial (\phi \tau_{zz})}{\partial z}\\
        \end{array}
    \right]_x
    = \frac{1}{\rho}
    \left(
        \frac{\partial (\phi \tau_{xx})}{\partial x}
        + \frac{\partial (\phi \tau_{xy})}{\partial y}
        + \frac{\partial (\phi \tau_{xz})}{\partial z}
    \right)

In a linear viscous fluid, the stress and strain rate
(:math:`\dot{\boldsymbol{\epsilon}}`) is linearly dependent, scaled by the
viscosity parameter :math:`\nu`:

.. math::
    \tau_{ij} = 2 \nu \dot{\epsilon}_{ij}
    = \nu \left(
    \frac{\partial v_i}{\partial x_j} + \frac{\partial v_j}{\partial x_i}
    \right)

With this relationship, the deviatoric stress tensor components can be
calculated as:

.. math::
    \tau_{xx} = 2 \nu \frac{\partial v_x}{\partial x} \qquad
    \tau_{yy} = 2 \nu \frac{\partial v_y}{\partial y} \qquad
    \tau_{zz} = 2 \nu \frac{\partial v_z}{\partial z}

    \tau_{xy} = \nu \left(
    \frac{\partial v_x}{\partial y} + \frac{\partial v_y}{\partial x} \right)

    \tau_{xz} = \nu \left(
    \frac{\partial v_x}{\partial z} + \frac{\partial v_z}{\partial x} \right)

    \tau_{yz} = \nu \left(
    \frac{\partial v_y}{\partial z} + \frac{\partial v_z}{\partial y} \right)

The above formulation of the fluid rheology assumes identical bulk and shear
viscosities.

The equations are solved in a similar manner for the other spatial components.
The partial differential terms in the equations presented above are found using
finite central differences.

Modifying the operator splitting methodology presented by Langtangen et al.
(2002), the predicted velocity :math:`\boldsymbol{v}^*` after a finite time step
:math:`\Delta t` is found by explicit integration of the momentum equation:

.. math::
    v_x^* = v_x^t + \Delta v_x

    \Rightarrow 
    v_x^* = v_x^t
    - \frac{\Delta t}{\Delta \phi} \nabla \cdot (\phi v_x \boldsymbol{v})
    - \frac{\beta \Delta t}{\rho \Delta \phi} \nabla p|_x
    + \frac{\Delta t}{\rho \Delta \phi}
      \left[ \nabla \cdot (\phi \boldsymbol{\tau}) \right]_x
    + \frac{\Delta t}{\Delta \phi} \phi g_x

The found velocity is only a prediction, since the estimate isn't constrained by
the continuity equation. The term :math:`\beta` is an adjustable, dimensionless
parameter in the range :math:`[0;1]`, and determines the importance of the old
pressure values in the solution procedure. A value of 0 corresponds to `Chorin's
projection method`_ originally described in `Chorin (1968)`_.







The solution of the Navier-Stokes equations is performed by operator splitting
methods.  The methodology presented by Langtangen et al. (2002) is for a viscous
fluid without particles. A velocity prediction after a forward step in time
(:math:`\Delta t`) in the momentum equation is found using an explicit scheme:

.. math::
    \bar{\boldsymbol{v}}^* = \bar{\boldsymbol{v}}^t
    - \Delta t \bar{\boldsymbol{v}}^t \cdot \nabla \bar{\boldsymbol{v}}^t
    - \Delta t \frac{\beta}{\rho} \nabla \bar{p}^t
    + \Delta t \nu \nabla^2 \bar{\boldsymbol{v}}^t
    + \Delta t \boldsymbol{f}_g^t

This predicted velocity does not account for the incompressibility condition.
The parameter :math:`\beta` is an adjustable, dimensionless relaxation
parameter. The above velocity prediction is modified to account for the presence
of particles and the fluid inviscidity:

.. math::
    \bar{\boldsymbol{v}}^* = \bar{\boldsymbol{v}}^t 
    - \Delta t \nabla \cdot (\phi^t \bar{\boldsymbol{v}}^t
      \otimes \bar{\boldsymbol{v}}^t)
    - \Delta t \frac{\beta}{\rho} \phi^t \nabla \bar{p}^t
    - \Delta t \boldsymbol{\bar{F}}_i^t
    + \Delta t \phi^t \boldsymbol{f}_g^t

The new velocities should fulfill the continuity (here incompressibility)
equation:

.. math::
    \frac{\Delta \phi^t}{\Delta t} + \nabla \cdot (\phi^t
    \bar{\boldsymbol{v}}^{t+\Delta t}) = 0

The divergence of a scalar and vector can be `split`_:

.. math::
    \phi^t \nabla \cdot \bar{\boldsymbol{v}}^{t+\Delta t} +
    \bar{\boldsymbol{v}}^{t+\Delta t} \cdot \nabla \phi^t
    + \frac{\Delta \phi^t}{\Delta t} = 0

The predicted velocity is corrected using the new pressure (Langtangen et al.
2002):

.. math::
    \bar{\boldsymbol{v}}^{t+\Delta t} = \bar{\boldsymbol{v}}^*
    - \frac{\Delta t}{\rho} \nabla \epsilon
    \quad \text{where} \quad
    \epsilon = p^{t+\Delta t} - \beta p^t

The above formulation of the future velocity is put into the continuity
equation:

.. math::
    \Rightarrow
    \phi^t \nabla \cdot
    \left( \bar{\boldsymbol{v}}^* - \frac{\Delta t}{\rho} \nabla \epsilon \right)
    +
    \left( \bar{\boldsymbol{v}}^* - \frac{\Delta t}{\rho} \nabla \epsilon \right)
    \cdot \nabla \phi^t + \frac{\Delta \phi^t}{\Delta t} = 0

.. math::
    \Rightarrow
    \phi^t \nabla \cdot
    \bar{\boldsymbol{v}}^* - \frac{\Delta t}{\rho} \phi^t \nabla^2 \epsilon
    + \nabla \phi^t \cdot \bar{\boldsymbol{v}}^*
    - \nabla \phi^t \cdot \nabla \epsilon \frac{\Delta t}{\rho}
    + \frac{\Delta \phi^t}{\Delta t} = 0

.. math::
    \Rightarrow
    \frac{\Delta t}{\rho} \phi^t \nabla^2 \epsilon
    = \phi^t \nabla \cdot \bar{\boldsymbol{v}}^*
    + \nabla \phi^t \cdot \bar{\boldsymbol{v}}^*
    - \nabla \phi^t \cdot \nabla \epsilon \frac{\Delta t}{\rho}
    + \frac{\Delta \phi^t}{\Delta t}

The pressure difference in time becomes a `Poisson equation`_ with added terms:

.. math::
    \Rightarrow
    \nabla^2 \epsilon
    = \frac{\nabla \cdot \bar{\boldsymbol{v}}^* \rho}{\Delta t}
    + \frac{\nabla \phi^t \cdot \bar{\boldsymbol{v}}^* \rho}{\Delta t \phi^t}
    - \frac{\nabla \phi^t \cdot \nabla \epsilon}{\phi^t}
    + \frac{\Delta \phi^t \rho}{\Delta t^2 \phi^t}

The right hand side of the above equation is termed the *forcing function*
:math:`f`, which is decomposed into two functions, :math:`f_1` and :math:`f_2`:

.. math::
    f_1 
    = \frac{\nabla \cdot \bar{\boldsymbol{v}}^* \rho}{\Delta t}
    + \frac{\nabla \phi^t \cdot \bar{\boldsymbol{v}}^* \rho}{\Delta t \phi^t}
    + \frac{\Delta \phi^t \rho}{\Delta t^2 \phi^t}

    f_2 =
    \frac{\nabla \phi^t \cdot \nabla \epsilon}{\phi^t}


During the `Jacobi iterative solution procedure`_ :math:`f_1` remains constant,
while :math:`f_2` changes value. For this reason, :math:`f_1` is found only at
the first iteration, while :math:`f_2` is updated every time. The value of the
forcing function is found as:

.. math::
    f = f_1 - f_2

Using second-order finite difference approximations of the Laplace operator
second-order partial derivatives, the differential equations become a system of
equations that is solved using `iteratively`_ using Jacobi updates. The total
number of unknowns is :math:`(n_x - 1)(n_y - 1)(n_z - 1)`.

The discrete Laplacian (approximation of the Laplace operator) can be obtained
by a finite-difference seven-point stencil in a three-dimensional, cubic
grid with cell spacing :math:`\Delta x, \Delta y, \Delta z`, considering the six
face neighbors:

.. math::
    \nabla^2 \epsilon_{i_x,i_y,i_z}  \approx 
    \frac{\epsilon_{i_x-1,i_y,i_z} - 2 \epsilon_{i_x,i_y,i_z}
    + \epsilon_{i_x+1,i_y,i_z}}{\Delta x^2}
    + \frac{\epsilon_{i_x,i_y-1,i_z} - 2 \epsilon_{i_x,i_y,i_z}
    + \epsilon_{i_x,i_y+1,i_z}}{\Delta y^2}

    + \frac{\epsilon_{i_x,i_y,i_z-1} - 2 \epsilon_{i_x,i_y,i_z}
    + \epsilon_{i_x,i_y,i_z+1}}{\Delta z^2}
    \approx f_{i_x,i_y,i_z}

Within a Jacobi iteration, the value of the unknowns (:math:`\epsilon^n`) is
used to find an updated solution estimate (:math:`\epsilon^{n+1}`).
The solution for the updated value takes the form:

.. math::
    \epsilon^{n+1}_{i_x,i_y,i_z}
    = \frac{-\Delta x^2 \Delta y^2 \Delta z^2 f_{i_x,i_y,i_z}
    + \Delta y^2 \Delta z^2 (\epsilon^n_{i_x-1,i_y,i_z} +
      \epsilon^n_{i_x+1,i_y,i_z})
    + \Delta x^2 \Delta z^2 (\epsilon^n_{i_x,i_y-1,i_z} +
      \epsilon^n_{i_x,i_y+1,i_z})
    + \Delta x^2 \Delta y^2 (\epsilon^n_{i_x,i_y,i_z-1} +
      \epsilon^n_{i_x,i_y,i_z+1})}
      {2 (\Delta x^2 \Delta y^2
      + \Delta x^2 \Delta z^2
      + \Delta y^2 \Delta z^2) }

The difference between the current and updated value is termed the *normalized
residual*:

.. math::
    r_{i_x,i_y,i_z} = \frac{(\epsilon^{n+1}_{i_x,i_y,i_z}
    - \epsilon^n_{i_x,i_y,i_z})^2}{(\epsilon^{n+1}_{i_x,i_y,i_z})^2}

Note that the :math:`\epsilon` values cannot be 0 due to the above normalization
of the residual.

The updated values are at the end of the iteration stored as the current values,
and the maximal value of the normalized residual is found. If this value is
larger than a tolerance criteria, the procedure is repeated. The iterative
procedure is ended if the number of iterations exceeds a defined limit. 

After the values of :math:`\epsilon` are found, they are used to find the new
pressures and velocities:

.. math::
    \bar{p}^{t+\Delta t} = \beta \bar{p}^t + \epsilon

.. math::
    \bar{\boldsymbol{v}}^{t+\Delta t} =
    \bar{\boldsymbol{v}}^* - \frac{\Delta t}{\rho} \nabla \epsilon




.. _Limache and Idelsohn (2006): http://www.cimec.org.ar/ojs/index.php/mc/article/view/486/464
.. _Cauchy stress tensor: https://en.wikipedia.org/wiki/Cauchy_stress_tensor
.. _`Chorin's projection method`: https://en.wikipedia.org/wiki/Projection_method_(fluid_dynamics)#Chorin.27s_projection_method
.. _`Chorin (1968)`: http://www.ams.org/journals/mcom/1968-22-104/S0025-5718-1968-0242392-2/S0025-5718-1968-0242392-2.pdf
.. _split: http://www.wolframalpha.com/input/?i=div(p+v)
.. _Poisson equation: https://en.wikipedia.org/wiki/Poisson's_equation
.. _`Jacobi iterative solution procedure`: http://www.rsmas.miami.edu/personal/miskandarani/Courses/MSC321/Projects/prjpoisson.pdf
.. _iteratively: https://en.wikipedia.org/wiki/Relaxation_(iterative_method)

