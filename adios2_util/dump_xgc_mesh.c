#include <stdio.h>
#include <stdlib.h>
#include "adios2_wrapper.h"

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("usage: ./dump-xgc-mesh <xgc.mesh.bp> <num_nodes>\n");
        exit(0);
    }
    MPI_Init( &argc, &argv);

    char* mesh_bp_file = argv[1];
    adios2_wrapper* w = new_adios2_wrapper(mesh_bp_file);
    if (w == NULL) {
        printf("ERROR: adios2_wrapper came back NULL\n");
        exit(-1);
    }

    size_t num_nodes = atoi(argv[2]);

    // The XGC mesh is always 2-Dimensional
    size_t dim2 = 2;
    double** mesh = adios2_read_2D_double_array(w, "/coordinates/values", num_nodes, dim2);

    for (int i = 0; i < num_nodes; i++)
        printf("%f,%f\n", mesh[i][0], mesh[i][1]);

    close_adios2_engine(w);

}
