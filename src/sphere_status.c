#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[])
{

    // Read path to current working directory
    char *cwd;
    cwd = getcwd(0, 0);
    if (!cwd) {  // Terminate program execution if path is not obtained
        fprintf(stderr, "getcwd failed");
        return 1; // Return unsuccessful exit status
    }

    // Simulation name/ID read from first input argument
    if (argc != 2) {
        fprintf(stderr, "You need to specify the simulation ID as an input "
                "parameter, e.g.\n%s particle_test\n", argv[0]);
        return 1;
    }

    char *sim_name = argv[1];

    // Open the simulation status file
    FILE *fp;
    char file[1000]; // Complete file path+name variable
    sprintf(file,"%s/output/%s.status.dat", cwd, sim_name);

    if ((fp = fopen(file, "rt"))) {
        float time_current;
        float time_percentage;
        unsigned int file_nr;

        if (fscanf(fp, "%f%f%d", &time_current, &time_percentage, &file_nr)
                != 3) {
            fprintf(stderr, "Error: could not parse file %s\n", file);
            return 1;
        }

        printf("Reading %s:\n"
                " - Current simulation time:  %f s\n"
                " - Percentage completed:     %f %%\n"
                " - Latest output file:       %s.output%05d.bin\n",
                file, time_current, time_percentage, sim_name, file_nr);

        fclose(fp);

        return 0; // Exit program successfully

    } else {
        fprintf(stderr, "Error: Could not open file %s\n", file);
        return 1;
    }
}
// vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
