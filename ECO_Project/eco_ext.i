%module eco_ext

%{
    #define SWIG_FILE_WITH_INIT
    #include "./eco_ext/eco_ext.h"
%}

%include "./eco_ext/numpy.i"

%init %{
    import_array();
%}

// %apply (double* INPLACE_ARRAY1, int DIM1) {(double* invec, int n)}
%apply (int* IN_ARRAY2, int DIM1, int DIM2) {(int *org_array, int org_dim_1, int org_dim_2)}
%apply (int* IN_ARRAY1, int DIM1) {(int *check_array, int check_dim)}


%include "./eco_ext/eco_ext.h"