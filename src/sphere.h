// Make sure the header is only included once
#ifndef SPHERE_H_
#define SPHERE_H_

#include <vector>

#include "datatypes.h"

// DEM class
class DEM {

    // Values and functions only accessible from the class internally
    private:

        // Input filename (full path)
        std::string inputbin;

        // Simulation ID
        std::string sid;

        // Output level
        int verbose;

        // Number of dimensions
        unsigned int nd;

        // Number of particles
        unsigned int np;

        // HOST STRUCTURES
        // Structure containing individual particle kinematics
        Kinematics k;	// host

        // Structure containing energy values
        Energies e;

        // Structure of global parameters
        Params params;

        // Structure containing spatial parameters
        Grid grid;

        // Structure of temporal parameters
        Time time;

        // Structure of wall parameters
        Walls walls;

        // Image structure (red, green, blue, alpa)
        rgba* img;
        unsigned int width;
        unsigned int height;


        // DEVICE ARRAYS
        Float4 *dev_x;
        Float2 *dev_xysum;
        Float4 *dev_vel;
        Float4 *dev_vel0;
        Float4 *dev_acc;
        Float4 *dev_force;
        Float4 *dev_angpos;
        Float4 *dev_angvel;
        Float4 *dev_angvel0;
        Float4 *dev_angacc;
        Float4 *dev_torque;
        unsigned int *dev_contacts;
        Float4 *dev_distmod;
        Float4 *dev_delta_t;
        Float *dev_es_dot;
        Float *dev_es;
        Float *dev_ev_dot;
        Float *dev_ev;
        Float *dev_p;
        Float4 *dev_x_sorted;
        Float4 *dev_vel_sorted;
        Float4 *dev_angvel_sorted;
        unsigned int *dev_gridParticleCellID;
        unsigned int *dev_gridParticleIndex;
        unsigned int *dev_cellStart;
        unsigned int *dev_cellEnd;
        int *dev_walls_wmode;
        Float4 *dev_walls_nx; // normal, pos.
        Float4 *dev_walls_mvfd; // Mass, velocity, force, dev. stress
        Float *dev_walls_force_partial; // Pre-sum per wall
        Float *dev_walls_force_pp; // Force per particle per wall
        Float *dev_walls_vel0; // Half-step velocity
        uint2 *dev_bonds;   // Particle bond pairs
        Float4 *dev_bonds_delta; // Particle bond displacement
        Float4 *dev_bonds_omega; // Particle bond rotation
        unsigned char *dev_img;
        float4 *dev_ray_origo;	// Ray data always single precision
        float4 *dev_ray_direction;


        // GPU initialization, must be called before startTime()
        void initializeGPU(void);

        // Copy all constant data to constant device memory
        void transferToConstantDeviceMemory(void);
        void rt_transferToConstantDeviceMemory(void);

        // Check values stored in constant device memory
        void checkConstantMemory(void);

        // Initialize camera values and transfer to constant device memory
        void cameraInit(const float3 eye,
                const float3 lookat, 
                const float imgw,
                const float focalLength);

        // Allocate global device memory to hold data
        void allocateGlobalDeviceMemory(void);
        void rt_allocateGlobalDeviceMemory(void);

        // Free dynamically allocated global device memory
        void freeGlobalDeviceMemory(void);
        void rt_freeGlobalDeviceMemory(void);

        // Copy non-constant data to global GPU memory
        void transferToGlobalDeviceMemory(void);

        // Copy non-constant data from global GPU memory to host RAM
        void transferFromGlobalDeviceMemory(void);
        void rt_transferFromGlobalDeviceMemory(void);

        // Find and return the max. radius
        Float r_max(void);

        // Write porosities found in porosity() to text file
        void writePorosities(
                const char *target,
                const int z_slices,
                const Float *z_pos,
                const Float *porosity);

        // Lattice-Boltzmann data arrays (D3Q19)
        Float  *f;          // Fluid distribution (f0..f18)
        Float  *f_new;      // t+deltaT fluid distribution (f0..f18)
        Float  *dev_f;      // Device equivalent
        Float  *dev_f_new;  // Device equivalent
        Float4 *v_rho;      // Fluid velocity v (xyz), and pressure rho (w) 
        Float4 *dev_v_rho;  // Device equivalent


    public:
        // Values and functions accessible from the outside

        // Constructor, some parameters with default values
        DEM(std::string inputbin, 
                const int verbosity = 1,
                const int checkVals = 1,
                const int dry = 0,
                const int initCuda = 1,
                const int transferConstMem = 1);

        // Destructor
        ~DEM(void);

        // Read binary input file
        void readbin(const char *target);

        // Write binary output file
        void writebin(const char *target);

        // Check numeric values of selected parameters
        void checkValues(void);

        // Report key parameter values to stdout
        void reportValues(void);

        // Iterate through time, using temporal limits
        // described in "time" struct.
        void startTime(void);

        // Render particles using raytracing
        void render(
                const int method = 1,
                const float maxval = 1.0e3f,
                const float lower_cutoff = 0.0f,
                const float focalLength = 1.0f,
                const unsigned int img_width = 800,
                const unsigned int img_height = 800);

        // Write image data to PPM file
        void writePPM(const char *target);

        // Calculate porosity with depth and save as text file
        void porosity(const int z_slices = 10);

        // find and return the min. position of any particle in each dimension
        Float3 minPos(void);

        // find and return the max. position of any particle in each dimension
        Float3 maxPos(void);

        // Find particle-particle intersections, saves the indexes
        // and the overlap sizes
        void findOverlaps(
                std::vector< std::vector<unsigned int> > &ij,
                std::vector< Float > &delta_n_ij);

        // Calculate force chains and save as Gnuplot script
        void forcechains(
                const std::string format = "interactive",
                const int threedim = 1,
                const double lower_cutoff = 0.0,
                const double upper_cutoff = 1.0e9);

        // Calculate Darcy fluid flow through material
        void startDarcy(
                const Float cellsizemultiplier = 1.0);
};



#endif
// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
