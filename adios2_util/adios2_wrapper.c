#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "utils.h"
#include "adios2_wrapper.h"


adios2_wrapper* new_adios2_wrapper(char* filename) {
    if (access (filename, F_OK) != 0 ) {
        fprintf(stderr,"FATAL: file %s does not exist.\n", filename);
        exit(1);
    }

    adios2_wrapper* w = (adios2_wrapper*)malloc(sizeof(adios2_wrapper));

    adios2_adios* reader = adios2_init(MPI_COMM_WORLD, adios2_debug_mode_off);

    w->filename = filename;
    w->io = adios2_declare_io(reader, "reader");
    w->engine = adios2_open(w->io, filename, adios2_mode_read);
    return w;
}


void close_adios2_engine(adios2_wrapper* w) {
    adios2_close(w->engine);
    free(w);
}


adios2_variable* get_adios2_var(adios2_wrapper* w, const char* varname){
    adios2_variable *var = adios2_inquire_variable(w->io, varname);
    if (var == NULL) {
        fprintf(
            stderr,
            "FATAL: adios2 variable \"%s\" does not exist in %s\n",
            varname,
            w->filename);
        exit(1);
    }
    return var;
}


void get_adios2_data(adios2_wrapper* w, adios2_variable* var, const char* varname, void* data) {
    adios2_error err = adios2_get(w->engine, var, data, adios2_mode_sync);
    if (err) {
        fprintf(
            stderr,
            "ERROR: error code %d caught when reading variable %s from %s\n",
            err, varname, w->filename);
    }
}


int adios2_read_int(adios2_wrapper* w, const char* varname) {
    adios2_variable* var = get_adios2_var(w, varname);
    int data;
    get_adios2_data(w, var, varname, &data);
    return data;
}


double adios2_read_double(adios2_wrapper* w, const char* varname) {
    adios2_variable* var = get_adios2_var(w, varname);
    double data;
    get_adios2_data(w, var, varname, &data);
    return data;
}


double* adios2_read_1D_double_array(adios2_wrapper* w, const char* varname,
                                const size_t count) {
    size_t start[1] = {0};
    size_t counts[1] = {count};
    adios2_variable* var = get_adios2_var(w, varname);
    adios2_set_selection(var, 1, start, counts);

    double* data = malloc_1D_double_array(count);
    get_adios2_data(w, var, varname, data);
    return data;
}

double* adios2_read_single_row_from_2D_double_array(adios2_wrapper* w, const char* varname,
                                const size_t count2, const size_t row_idx) {
    size_t start[2] = {row_idx, 0};

    // read exactly 1 row
    size_t count[2] = {1, count2};


    adios2_variable* var = get_adios2_var(w, varname);
    adios2_set_selection(var, 2, start, count);
    double** tmp = malloc_2D_double_array(1, count2);
    get_adios2_data(w, var, varname, tmp[0]);

    return tmp[0];
}


double** adios2_read_2D_double_array(adios2_wrapper* w, const char* varname,
                                const size_t count1, const size_t count2) {
    size_t start[2] = {0, 0};
    size_t count[2] = {count1, count2};

    adios2_variable* var = get_adios2_var(w, varname);
    adios2_set_selection(var, 2, start, count);

    // We use malloc_1D here instead of malloc_2D because Adios2 requires a single
    // contiguous section of memory to write to. malloc_2D constructs a 2D matrix from
    // several calls to malloc.
    double* data = malloc_1D_double_array(count1 * count2);
    get_adios2_data(w, var, varname, data);

    // Now, construct a 2D array out of this 1D
    double** results = malloc_2D_double_array(count1, count2);
    for (int i = 0; i < count1; i++)
        for (int j = 0; j < count2; j++)
            results[i][j] = data[i*count2 + j];

    free(data);
    return results;
}

double** adios2_extract_2D_array_from_3D_array(adios2_wrapper* w, const char* varname,
                                const size_t count1, const size_t count3,
                                const size_t start2) {
    size_t start[3] = {0, start2, 0};
    size_t count[3] = {count1, 1, count3};

    adios2_variable* var = get_adios2_var(w, varname);
    adios2_set_selection(var, 3, start, count);

    // We use malloc_1D here instead of malloc_2D because Adios2 requires a single
    // contiguous section of memory to write to. malloc_2D constructs a 2D matrix from
    // several calls to malloc.
    double* data = malloc_1D_double_array(count1 * count3);
    get_adios2_data(w, var, varname, data);

    double** results = malloc_2D_double_array(count1, count3);
    for (int i = 0; i < count1; i++)
        for (int j = 0; j < count3; j++)
            results[i][j] = data[i*count3 + j];

    free(data);
    return results;
}

int** adios2_read_2D_int_array(adios2_wrapper* w, const char* varname,
                                const size_t count1, const size_t count2) {
    size_t start[2] = {0, 0};
    size_t count[2] = {count1, count2};

    adios2_variable* var = get_adios2_var(w, varname);
    adios2_set_selection(var, 2, start, count);

    // We use malloc_1D here instead of malloc_2D because Adios2 requires a single
    // contiguous section of memory to write to. malloc_2D constructs a 2D matrix from
    // several calls to malloc.
    int* data = malloc_1D_int_array(count1 * count2);
    get_adios2_data(w, var, varname, data);

    // Now, construct a 2D array out of this 1D
    int** results = malloc_2D_int_array(count1, count2);
    for (int i = 0; i < count1; i++)
        for (int j = 0; j < count2; j++)
            results[i][j] = data[i*count2 + j];

    free(data);
    return results;
}
