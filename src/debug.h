#ifndef DEBUG_H_
#define DEBUG_H_

// Enable profiling of kernel runtimes?
// 0: No (default)
// 1: Yes
#define PROFILING 1

// Output information about contacts to stdout?
// 0: No (default)
// 1: Yes
#define CONTACTINFO 0

// The number of fluid solver iterations to perform between checking the norm.
// residual value
const unsigned int nijacnorm = 10;

// Write max. residual during the latest solution loop to logfile
// 'max_res_norm.dat'
// 0: False, 1: True
const int write_res_log = 0;

// Report epsilon values during Jacobi iterations to stdout
// 0: False, 1: True
const int report_epsilon = 0;
const int report_even_more_epsilon = 0;

// Report the number of iterations it took before convergence to logfile
// 'output/<sid>-conv.dat'
// 0: False, 1: True
const int write_conv_log = 1;

// The interval between iteration number reporting in 'output/<sid>-conv.log'
const int conv_log_interval = 10;
//const int conv_log_interval = 1;

#endif
