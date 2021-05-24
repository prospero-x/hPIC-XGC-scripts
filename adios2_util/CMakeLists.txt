cmake_minimum_required(VERSION 3.16.3)
project (xgc_helper_scripts)

set(CMAKE_BUILD_TYPE Release CACHE STRING "")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -O0 -Wall -g")
################################################################################
# Grab adios2 libraries
find_package(ADIOS2 REQUIRED)


################################################################################
# Compile source code
add_executable(dump-xgc-mesh
    adios2_wrapper.c
    utils.c
)

set(HPIC_1D3V_LIBRARIES
  -lm
  "${ADIOS2_LIBRARIES}")

target_sources(dump-xgc-mesh PRIVATE dump_xgc_mesh.c)

target_link_libraries(dump-xgc-mesh ${HPIC_1D3V_LIBRARIES})

