#ifndef ADIOS2_WRAPPER_H
#define ADIOS2_WRAPPER_H

#include <adios2_c.h>

typedef struct {
    char* filename;
    adios2_io* io;
    adios2_engine* engine;
} adios2_wrapper;

adios2_wrapper* new_adios2_wrapper(char* filename);
void close_adios2_engine(adios2_wrapper*);
adios2_variable* get_adios2_var(adios2_wrapper* w, const char* varname);
void get_adios2_data(adios2_wrapper* w, adios2_variable* var, const char* varname, void* data);
int adios2_read_int(adios2_wrapper* w, const char* varname);
double adios2_read_double(adios2_wrapper* w, const char* varname);


double* adios2_read_1D_double_array(adios2_wrapper* w, const char* varname, const size_t count);
double* adios2_read_single_row_from_2D_double_array(adios2_wrapper* w, const char* varname, const size_t count2, const size_t row_idx);
double** adios2_read_2D_double_array(adios2_wrapper* w, const char* varname, const size_t count1, const size_t count2);
double** adios2_extract_2D_array_from_3D_array(adios2_wrapper* w, const char* varname, const size_t count1, const size_t count3, const size_t start2);

int** adios2_read_2D_int_array(adios2_wrapper* w, const char* varname, const size_t count1, const size_t count2);
#endif /* adios2_wrapper.h */
