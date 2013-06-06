#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

#include "typedefs.h"
#include "datatypes.h"
#include "constants.h"
#include "sphere.h"

// Initialize memory
void DEM::initDarcyMem()
{
    unsigned int ncells = d_nx*d_ny*d_nz;
    d_H = new Float[ncells]; // hydraulic pressure matrix
    d_V = new Float3[ncells]; // Cell hydraulic velocity
    d_dH = new Float3[ncells]; // Cell spatial gradient in hydraulic pressures
    d_K = new Float[ncells]; // hydraulic conductivity matrix
    d_S = new Float[ncells]; // hydraulic storativity matrix
    d_W = new Float[ncells]; // hydraulic recharge
    d_n = new Float[ncells]; // cell porosity
}

// Free memory
void DEM::freeDarcyMem()
{
    free(d_H);
    free(d_V);
    free(d_dH);
    free(d_K);
    free(d_S);
    free(d_W);
    free(d_n);
}

// 3D index to 1D index
unsigned int DEM::idx(
        const unsigned int x,
        const unsigned int y,
        const unsigned int z)
{
    return x + d_nx*y + d_nx*d_ny*z;
}

// Set initial values
void DEM::initDarcyVals()
{
    unsigned int ix, iy, iz;
    for (ix=0; ix<d_nx; ++ix) {
        for (iy=0; iy<d_ny; ++iy) {
            for (iz=0; iz<d_nz; ++iz) {

                // Initial hydraulic head [m]
                //d_H[idx(ix,iy,iz)] = 1.0;
                // read from input binary

                // Hydraulic conductivity [m/s]
                d_K[idx(ix,iy,iz)] = 1.5;

                // Hydraulic storativity [-]
                d_S[idx(ix,iy,iz)] = 7.5e-3;

                // Hydraulic recharge [Pa/s]
                d_W[idx(ix,iy,iz)] = 0.0;
            }
        }
    }
}

Float DEM::minVal3dArr(Float* arr)
{
    Float minval = 1e16; // a large val
    Float val;
    unsigned int ix, iy, iz;
    for (ix=0; ix<d_nx; ++ix) {
        for (iy=0; iy<d_ny; ++iy) {
            for (iz=0; iz<d_nz; ++iz) {
                val = arr[idx(ix,iy,iz)];
                if (minval > val)
                    minval = val;
            }
        }
    }
}

// Find the spatial gradient in pressures per cell
void DEM::findDarcyGradients()
{
    // Cell sizes squared
    const Float dx2 = d_dx*d_dx;
    const Float dy2 = d_dy*d_dy;
    const Float dz2 = d_dz*d_dz;

    Float H;
    unsigned int ix, iy, iz, cellidx;

    for (ix=1; ix<d_nx-1; ++ix) {
        for (iy=1; iy<d_ny-1; ++iy) {
            for (iz=1; iz<d_nz-1; ++iz) {

                cellidx = idx(ix,iy,iz);

                H = d_H[cellidx];   // cell hydraulic pressure

                // Second order central difference
                d_dH[cellidx].x
                 = (d_H[idx(ix+1,iy,iz)] - 2.0*H + d_H[idx(ix-1,iy,iz)])/dx2;
                
                d_dH[cellidx].y
                 = (d_H[idx(ix,iy+1,iz)] - 2.0*H + d_H[idx(ix,iy-1,iz)])/dy2;

                d_dH[cellidx].z
                 = (d_H[idx(ix,iy,iz+1)] - 2.0*H + d_H[idx(ix,iy,iz-1)])/dz2;
            }
        }
    }
}


// Set the gradient to 0.0 in all dimensions at the boundaries
void DEM::setDarcyBCNeumannZero()
{
    Float3 z3 = MAKE_FLOAT3(0.0, 0.0, 0.0);
    unsigned int ix, iy, iz;
    unsigned int nx = d_nx-1;
    unsigned int ny = d_ny-1;
    unsigned int nz = d_nz-1;

    // I don't care that the values at four edges are written twice

    // x-y plane at z=0 and z=d_dz-1
    for (ix=0; ix<d_nx; ++ix) {
        for (iy=0; iy<d_ny; ++iy) {
            d_dH[idx(ix,iy, 0)] = z3;
            d_dH[idx(ix,iy,nz)] = z3;
        }
    }

    // x-z plane at y=0 and y=d_dy-1
    for (ix=0; ix<d_nx; ++ix) {
        for (iz=0; iz<d_nz; ++iz) {
            d_dH[idx(ix, 0,iz)] = z3;
            d_dH[idx(ix,ny,iz)] = z3;
        }
    }

    // y-z plane at x=0 and x=d_dx-1
    for (iy=0; iy<d_ny; ++iy) {
        for (iz=0; iz<d_nz; ++iz) {
            d_dH[idx( 0,iy,iz)] = z3;
            d_dH[idx(nx,iy,iz)] = z3;
        }
    }
}


// Perform an explicit step.
// Boundary conditions are fixed gradient values (Neumann)
void DEM::explDarcyStep()
{
    // Cell dims squared
    const Float dx2 = d_dx*d_dx;
    const Float dy2 = d_dy*d_dy;
    const Float dz2 = d_dz*d_dz;

    // Find cell gradients
    findDarcyGradients();
    setDarcyBCNeumannZero();

    // Explicit 3D finite difference scheme
    // new = old + gradient*timestep
    unsigned int ix, iy, iz, cellidx;
    Float K, H;
    Float dt = time.dt;
    for (ix=0; ix<d_nx; ++ix) {
        for (iy=0; iy<d_ny; ++iy) {
            for (iz=0; iz<d_nz; ++iz) {

                cellidx = idx(ix,iy,iz);

                K = d_K[cellidx];   // cell hydraulic conductivity
                H = d_H[cellidx];   // cell hydraulic pressure

                d_H[cellidx]
                    += d_W[cellidx]*dt  // cell recharge
                    + K*dt *            // diffusivity term
                    (d_dH[cellidx].x + d_dH[cellidx].y + d_dH[cellidx].z);
            }
        }
    }

    // Find macroscopic cell fluid velocities
    findDarcyVelocities();
}

// Print array values to file stream (stdout, stderr, other file)
void DEM::printDarcyArray(FILE* stream, Float* arr)
{
    unsigned int x, y, z;
    for (z=0; z<d_nz; z++) {
        for (y=0; y<d_ny; y++) {
            for (x=0; x<d_nx; x++) {
                fprintf(stream, "%f\t", arr[idx(x,y,z)]);
            }
            fprintf(stream, "\n");
        }
        fprintf(stream, "\n");
    }
}

// Overload printDarcyArray to add optional description
void DEM::printDarcyArray(FILE* stream, Float* arr, std::string desc)
{
    std::cout << "\n" << desc << ":\n";
    printDarcyArray(stream, arr);
}

// Print array values to file stream (stdout, stderr, other file)
void DEM::printDarcyArray(FILE* stream, Float3* arr)
{
    unsigned int x, y, z;
    for (z=0; z<d_nz; z++) {
        for (y=0; y<d_ny; y++) {
            for (x=0; x<d_nx; x++) {
                fprintf(stream, "%f,%f,%f\t",
                        arr[idx(x,y,z)].x,
                        arr[idx(x,y,z)].y,
                        arr[idx(x,y,z)].z);
            }
            fprintf(stream, "\n");
        }
        fprintf(stream, "\n");
    }
}

// Overload printDarcyArray to add optional description
void DEM::printDarcyArray(FILE* stream, Float3* arr, std::string desc)
{
    std::cout << "\n" << desc << ":\n";
    printDarcyArray(stream, arr);
}

// Find cell velocity
void DEM::findDarcyVelocities()
{
    // Flux [m/s]: q = -k/nu * dH
    // Pore velocity [m/s]: v = q/n
    Float3 q, v, dH;

    // Dynamic viscosity
    Float nu = params.nu;

    // Porosity [-]: n

    unsigned int ix, iy, iz, cellidx;
    for (ix=0; ix<d_nx; ++ix) {
        for (iy=0; iy<d_ny; ++iy) {
            for (iz=0; iz<d_nz; ++iz) {
                
                cellidx = idx(ix,iy,iz);
                dH = d_dH[cellidx];

                // Approximate cell porosity
                Float n = cellPorosity(ix, iy, iz);

                // Calculate flux
                // The sign might need to be reversed, depending on the
                // grid orientation
                q.x = -d_K[cellidx]/nu * dH.x;
                q.y = -d_K[cellidx]/nu * dH.y;
                q.z = -d_K[cellidx]/nu * dH.z;
                
                // Calculate velocity
                v.x = q.x/n;
                v.y = q.y/n;
                v.z = q.z/n;
                d_V[cellidx] = v;
            }
        }
    }
}

// Return the lower corner coordinates of a cell
Float3 DEM::cellMinBoundaryDarcy(
        const unsigned int x,
        const unsigned int y,
        const unsigned int z)
{
    const Float3 x_min = {x*d_dx, y*d_dy, z*d_dz};
    return x_min;
}

// Return the lower corner coordinates of a cell
Float3 DEM::cellMaxBoundaryDarcy(
        const unsigned int x,
        const unsigned int y,
        const unsigned int z)
{
    const Float3 x_max = {(x+1)*d_dx, (y+1)*d_dy, (z+1)*d_dz};
    return x_max;
}

// Return the volume of a cell
Float DEM::cellVolumeDarcy()
{
    const Float cell_volume = d_dx*d_dy*d_dz;
    return cell_volume;
}

// Find the porosity of a target cell
Float DEM::cellPorosity(
        const unsigned int x,
        const unsigned int y,
        const unsigned int z)
{
    const Float3 x_min = cellMinBoundaryDarcy(x,y,z);
    const Float3 x_max = cellMaxBoundaryDarcy(x,y,z);
    Float cell_volume = cellVolumeDarcy();
    Float void_volume = cell_volume;

    unsigned int i;
    Float4 xr;
    for (i=0; i<np; ++i) {

        // Read the position and radius
        xr = k.x[i];

        if (xr.x >= x_min.x && xr.y >= x_min.y && xr.z >= x_min.z
                && xr.x < x_max.x && xr.y < x_max.y && xr.z < x_max.z) {
            void_volume -= 4.0/3.0*M_PI*xr.w*xr.w*xr.w;
        }
    }

    // Return the porosity, which should always be between 0.0 and 1.0
    Float n = fmin(1.0, fmax(0.0, (void_volume)/cell_volume));
    d_n[idx(x,y,z)] = n;
    return n;
}

// Find particles with centres inside a spatial interval
// NOTE: This function is untested and unused
std::vector<unsigned int> DEM::particlesInCell(
        const Float3 min, const Float3 max)
{
    // Particles radii inside cell will be stored in this vector
    std::vector<unsigned int> pidx;

    unsigned int i;
    Float4 x;
    for (i=0; i<np; ++i) {

        // Read the position
        x = k.x[i];

        if (x.x >= min.x && x.y >= min.y && x.z >= min.z
                && x.x < max.x && x.y < max.y && x.z < max.z) {
            pidx.push_back(i);
        }
    }
}

// Add fluid drag to the particles inside each cell
void DEM::fluidDragDarcy()
{
    unsigned int ix, iy, iz, cellidx;
    for (ix=0; ix<d_nx; ++ix) {
        for (iy=0; iy<d_ny; ++iy) {
            for (iz=0; iz<d_nz; ++iz) {


            }
        }
    }
}

// Solve Darcy flow on a regular, cubic grid
void DEM::initDarcy(const Float cellsizemultiplier)
{
    if (params.nu <= 0.0) {
        std::cerr << "Error in initDarcy. The dymamic viscosity (params.nu), "
            << "should be larger than 0.0, but is " << params.nu << std::endl;
        exit(1);
    }

    // Number of cells
    d_nx = floor(grid.num[0]*cellsizemultiplier);
    d_ny = floor(grid.num[1]*cellsizemultiplier);
    d_nz = floor(grid.num[2]*cellsizemultiplier);

    // Cell size 
    d_dx = grid.L[0]/d_nx;
    d_dy = grid.L[1]/d_ny;
    d_dz = grid.L[2]/d_nz;

    if (verbose == 1) {
        std::cout << "  - Fluid grid dimensions: "
            << d_nx << "*"
            << d_ny << "*"
            << d_nz << std::endl;
        std::cout << "  - Fluid grid cell size: "
            << d_dx << "*"
            << d_dy << "*"
            << d_dz << std::endl;
    }

    initDarcyMem();
    initDarcyVals();
}

// Print final heads and free memory
void DEM::endDarcy()
{
    //printDarcyArray(stdout, d_H, "d_H");
    //printDarcyArray(stdout, d_V, "d_V");
    //printDarcyArray(stdout, d_n, "d_n");
    freeDarcyMem();
}

// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
