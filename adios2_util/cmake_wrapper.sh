#!/usr/bin/env bash

# Set these according to your system
ADIOS2_ROOT=~/ADIOS2
CMAKE_BUILD_TYPE=Debug

REST_OF_CMAKE_ARGS="$@"

cmake . \
    -DADIOS2_ROOT=$ADIOS2_ROOT \
    -DCMAKE_BUILD_TYPE=$CMAKE_BUILD_TYPE \
    "$REST_OF_CMAKE_ARGS"
