#ifndef INTEGRATION_CUH_
#define INTEGRATION_CUH_

// integration.cuh
// Functions responsible for temporal integration

// Second order integration scheme based on Taylor expansion of particle kinematics. 
// Kernel executed on device, and callable from host only.
__global__ void integrate(Float4* dev_x_sorted, Float4* dev_vel_sorted, // Input
        Float4* dev_angvel_sorted,
        Float4* dev_x, Float4* dev_vel, Float4* dev_angvel, // Output
        Float4* dev_force, Float4* dev_torque, Float4* dev_angpos, // Input
        Float4* dev_acc, Float4* dev_angacc,
        Float4* dev_vel0, Float4* dev_angvel0,
        Float2* dev_xysum,
        unsigned int* dev_gridParticleIndex, // Input: Sorted-Unsorted key
        unsigned int iter)
{
    unsigned int idx = threadIdx.x + blockIdx.x * blockDim.x; // Thread id

    if (idx < devC_np) { // Condition prevents block size error

        // Copy data to temporary arrays to avoid any potential read-after-write, 
        // write-after-read, or write-after-write hazards. 
        unsigned int orig_idx = dev_gridParticleIndex[idx];
        Float4 force   = dev_force[orig_idx];
        Float4 torque  = dev_torque[orig_idx];
        Float4 angpos  = dev_angpos[orig_idx];
        const Float4 acc0    = dev_acc[orig_idx];
        const Float4 angacc0 = dev_angacc[orig_idx];
        //Float4 vel0    = dev_vel0[orig_idx];
        //Float4 angvel0 = dev_angvel0[orig_idx];
        Float4 x       = dev_x_sorted[idx];
        Float4 vel     = dev_vel_sorted[idx];
        Float4 angvel  = dev_angvel_sorted[idx];
        const Float  radius  = x.w;

        Float2 xysum  = MAKE_FLOAT2(0.0f, 0.0f);

        Float4 acc, angacc;
        if (iter == 0) {
            // in the first iterations, the accelerations havn't been set yet.
            // Therefore, they are defined.
            acc = MAKE_FLOAT4(0.0, 0.0, 0.0, 0.0);
            angacc = MAKE_FLOAT4(0.0, 0.0, 0.0, 0.0);
        }

        // Coherent read from constant memory to registers
        const Float dt = devC_dt;
        const Float3 origo = MAKE_FLOAT3(
                devC_grid.origo[0],
                devC_grid.origo[1],
                devC_grid.origo[2]); 
        const Float3 L = MAKE_FLOAT3(
                devC_grid.L[0],
                devC_grid.L[1],
                devC_grid.L[2]);
        const Float rho = devC_params.rho;

        // Particle mass
        Float m = 4.0/3.0 * PI * radius*radius*radius * rho;

        // Update acceleration of particle
        acc.x = force.x*dt + devC_params.g[0];
        acc.y = force.y*dt + devC_params.g[1];
        acc.z = force.z*dt + devC_params.g[2];

        // Update angular acceleration of particle 
        // (angacc = (total moment)/Intertia, intertia = 2/5*m*r^2)
        angacc.x = torque.x * 1.0 / (2.0/5.0 * m * radius*radius);
        angacc.y = torque.y * 1.0 / (2.0/5.0 * m * radius*radius);
        angacc.z = torque.z * 1.0 / (2.0/5.0 * m * radius*radius);

        // Check if particle has a fixed horizontal velocity
        if (vel.w > 0.0f) {

            // Zero horizontal acceleration and disable
            // gravity to counteract segregation.
            // Particles may move in the z-dimension,
            // to allow for dilation.
            acc.x = 0.0;
            acc.y = 0.0;
            acc.z -= devC_params.g[2];

            // Zero the angular acceleration
            angacc = MAKE_FLOAT4(0.0, 0.0, 0.0, 0.0);
        }

        // Velocity Verlet algorithm using old and new accelerations
        pos.x += vel.x*dt + 0.5*acc0.x*dt*dt;
        pos.y += vel.y*dt + 0.5*acc0.y*dt*dt;
        pos.z += vel.z*dt + 0.5*acc0.z*dt*dt;

        angpos.x += angvel.x*dt + 0.5*angacc0.x*dt*dt;
        angpos.y += angvel.y*dt + 0.5*angacc0.y*dt*dt;
        angpos.z += angvel.z*dt + 0.5*angacc0.z*dt*dt;

        vel.x += (acc0.x + acc.x)/2.0*dt;
        vel.y += (acc0.y + acc.y)/2.0*dt;
        vel.z += (acc0.z + acc.z)/2.0*dt;

        angvel.x += (angacc0.x + angacc.x)/2.0*dt;
        angvel.y += (angacc0.y + angacc.y)/2.0*dt;
        angvel.z += (angacc0.z + angacc.z)/2.0*dt;

        // Move particles outside the domain across periodic boundaries
        if (devC_grid.periodic == 1) {
            if (x.x < origo.x)
                x.x += L.x;
            if (x.x > L.x)
                x.x -= L.x;
            if (x.y < origo.y)
                x.y += L.y;
            if (x.y > L.y)
                x.y -= L.y;
        } else if (devC_grid.periodic == 2) {
            if (x.x < origo.x)
                x.x += L.x;
            if (x.x > L.x)
                x.x -= L.x;
        }

        //// Half-step leapfrog Verlet integration scheme ////
        // Update half-step linear velocities
        /*vel0.x += acc.x * dt;
        vel0.y += acc.y * dt;
        vel0.z += acc.z * dt;

        // Update half-step angular velocities
        angvel0.x += angacc.x * dt;
        angvel0.y += angacc.y * dt;
        angvel0.z += angacc.z * dt;*/

        // Update positions
        //x.x += vel0.x * dt;
        //x.y += vel0.y * dt;
        //x.z += vel0.z * dt;

        // Update angular positions
        //angpos.x += angvel0.x * dt;
        //angpos.y += angvel0.y * dt;
        //angpos.z += angvel0.z * dt;

        // Update full-step linear velocity
        //vel.x = vel0.x + 0.5 * acc.x * dt;
        //vel.y = vel0.y + 0.5 * acc.y * dt;
        //vel.z = vel0.z + 0.5 * acc.z * dt;

        // Update full-step angular velocity
        //angvel.x = angvel0.x + 0.5 * angacc.x * dt;
        //angvel.y = angvel0.y + 0.5 * angacc.y * dt;
        //angvel.z = angvel0.z + 0.5 * angacc.z * dt;

        /*
        //// First-order Euler integration scheme ///
        // Update angular position
        angpos.x += angvel.x * dt;
        angpos.y += angvel.y * dt;
        angpos.z += angvel.z * dt;

        // Update position
        x.x += vel.x * dt;
        x.y += vel.y * dt;
        x.z += vel.z * dt;
         */

        /*
        /// Second-order scheme based on Taylor expansion ///
        // Update angular position
        angpos.x += angvel.x * dt + angacc.x * dt*dt * 0.5;
        angpos.y += angvel.y * dt + angacc.y * dt*dt * 0.5;
        angpos.z += angvel.z * dt + angacc.z * dt*dt * 0.5;

        // Update position
        x.x += vel.x * dt + acc.x * dt*dt * 0.5;
        x.y += vel.y * dt + acc.y * dt*dt * 0.5;
        x.z += vel.z * dt + acc.z * dt*dt * 0.5;
         */

        /*
        // Update angular velocity
        angvel.x += angacc.x * dt;
        angvel.y += angacc.y * dt;
        angvel.z += angacc.z * dt;

        // Update linear velocity
        vel.x += acc.x * dt;
        vel.y += acc.y * dt;
        vel.z += acc.z * dt;
         */

        // Add x-displacement for this time step to 
        // sum of x-displacements
        //x.w += vel.x * dt + (acc.x * dt*dt)/2.0f;
        xysum.x += vel.x*dt + 0.5*acc0.x*dt*dt;
        xysum.y += vel.y*dt + 0.5*acc0.y*dt*dt;

        // Hold threads for coalesced write
        __syncthreads();

        // Store data in global memory at original, pre-sort positions
        dev_xysum[orig_idx]  += xysum;
        dev_acc[orig_idx]     = acc;
        dev_angacc[orig_idx]  = angacc;
        dev_angvel[orig_idx]  = angvel;
        dev_vel[orig_idx]     = vel;
        dev_angpos[orig_idx]  = angpos;
        dev_x[orig_idx]       = x;
    } 
} // End of integrate(...)


// Reduce wall force contributions from particles to a single value per wall
__global__ void summation(Float* in, Float *out)
{
    __shared__ Float cache[256];
    unsigned int idx = threadIdx.x + blockIdx.x * blockDim.x;
    unsigned int cacheIdx = threadIdx.x;

    Float temp = 0.0f;
    while (idx < devC_np) {
        temp += in[idx];
        idx += blockDim.x * gridDim.x;
    }

    // Set the cache values
    cache[cacheIdx] = temp;

    __syncthreads();

    // For reductions, threadsPerBlock must be a power of two
    // because of the following code
    unsigned int i = blockDim.x/2;
    while (i != 0) {
        if (cacheIdx < i)
            cache[cacheIdx] += cache[cacheIdx + i];
        __syncthreads();
        i /= 2;
    }

    // Write sum for block to global memory
    if (cacheIdx == 0)
        out[blockIdx.x] = cache[0];
}

// Update wall positions
__global__ void integrateWalls(
        Float4* dev_walls_nx,
        Float4* dev_walls_mvfd,
        int* dev_walls_wmode,
        Float* dev_walls_force_partial,
        Float* dev_walls_vel0,
        unsigned int blocksPerGrid,
        Float t_current)
{
    unsigned int idx = threadIdx.x + blockIdx.x * blockDim.x; // Thread id

    if (idx < devC_nw) { // Condition prevents block size error

        // Copy data to temporary arrays to avoid any potential read-after-write, 
        // write-after-read, or write-after-write hazards. 
        Float4 w_nx   = dev_walls_nx[idx];
        Float4 w_mvfd = dev_walls_mvfd[idx];
        int wmode = dev_walls_wmode[idx];  // Wall BC, 0: fixed, 1: devs, 2: vel
        Float vel0 = dev_walls_vel0[idx];
        Float acc;

        if (wmode == 0) // Wall fixed: do nothing
            return;

        // Find the final sum of forces on wall
        w_mvfd.z = 0.0;
        for (int i=0; i<blocksPerGrid; ++i) {
            w_mvfd.z += dev_walls_force_partial[i];
        }

        Float dt = devC_dt;

        // Normal load = Deviatoric stress times wall surface area,
        // directed downwards.
        Float sigma_0 = w_mvfd.w + devC_params.devs_A * sin(2.0 * 3.141596654 * devC_params.devs_f * t_current);
        Float N = -sigma_0*devC_grid.L[0]*devC_grid.L[1];

        // Calculate resulting acceleration of wall
        // (Wall mass is stored in x component of position Float4)
        acc = (w_mvfd.z + N)/w_mvfd.x;

        // If Wall BC is controlled by velocity, it should not change
        if (wmode == 2) { 
            acc = 0.0;
        }

        //// Half-step leapfrog Verlet integration scheme ////
        
        // Update half-step velocity
        vel0 += acc * dt;

        // Update position. Second-order scheme based on Taylor expansion 
        //w_nx.w += w_mvfd.y * dt + (acc * dt*dt)/2.0;

        // Update position
        w_nx.w += vel0 * dt;

        // Update position. First-order Euler integration scheme
        //w_nx.w += w_mvfd.y * dt;

        // Update linear velocity
        //w_mvfd.y += acc * dt;
        w_mvfd.y = vel0 + 0.5 * acc * dt;

        //cuPrintf("\nwall %d, wmode = %d, force = %f, acc = %f\n", idx, wmode, w_mvfd.z, acc);

        // Store data in global memory
        dev_walls_nx[idx]   = w_nx;
        dev_walls_mvfd[idx] = w_mvfd;
        dev_walls_vel0[idx] = vel0;
    }
} // End of integrateWalls(...)


#endif
// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
