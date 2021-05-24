#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

void free_data_2D_int_array(int **data, size_t xlen)
{
    size_t i;

    for (i=0; i < xlen; ++i) {
        if (data[i] != NULL) {
            free(data[i]);
        }
    }
    free(data);
}

void free_data_2D_double_array(double **data, size_t xlen)
{
    size_t i;

    for (i=0; i < xlen; ++i) {
        if (data[i] != NULL) {
            free(data[i]);
        }
    }
    free(data);
}


//-----------------------------------------------------------------------//
int *malloc_1D_int_array(size_t xlen)
{
  int *a;
  if ((a = (int *) malloc(xlen * sizeof *a)) == NULL) {
    perror("malloc 1 on 1D data structure");
    return NULL;
  }
  return a;
}
//-----------------------------------------------------------------------//
int **malloc_2D_int_array(size_t xlen, size_t ylen)
{
  int **a;
  size_t i;

  if ((a = (int **) malloc(xlen * sizeof *a)) == NULL) {
    perror("malloc 1 on 2D data structure");
    return NULL;
  }

  for (i=0; i < xlen; ++i)
    a[i] = NULL;

  for (i=0; i < xlen; ++i)
    if ((a[i] = (int *) malloc(ylen * sizeof *a[i])) == NULL) {
      perror("malloc 2 on 2D data structure");
      free_data_2D_int_array(a, xlen);
      return NULL;
    }

  return a;
}
double *malloc_1D_double_array(size_t xlen)
{
  double *a;
  if ((a = (double*) malloc(xlen * sizeof *a)) == NULL) {
    perror("malloc 1 on 1D data structure");
    return NULL;
  }
  return a;
}
//-----------------------------------------------------------------------//
double **malloc_2D_double_array(size_t xlen, size_t ylen)
{
  double **a;
  size_t i;

  if ((a = (double **) malloc(xlen * sizeof *a)) == NULL) {
    perror("malloc 1 on 2D data structure");
    return NULL;
  }

  for (i=0; i < xlen; ++i)
    a[i] = NULL;

  for (i=0; i < xlen; ++i)
    if ((a[i] = (double *) malloc(ylen * sizeof *a[i])) == NULL) {
      perror("malloc 2 on 2D data structure");
      free_data_2D_double_array(a, xlen);
      return NULL;
    }

  return a;
}
