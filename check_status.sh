#!/usr/bin/env bash

# This script is meant to be run DURING hPIC simulations, ON LCPP boxes, in order
# to see which hPIC simulations are complete and which ones are still running.
# It's meant to be a more accurate representation than "$ htop" or
# "$ ps -ef | grep hpic | grep <MY_SIMULATION_PATTERNS>".
#
# It assumes that, before a particular hPIC simulation, a file named
# "simulation-start" was created in the particular hPIC simualtion subdirectory,
# containing a single line date time string in the format %Y-%m-%dT%H:%S-%Z.
# Similarlty, it assumes that ones an hPIC simulation is complete, a similar
# file named "simulation-complete" is created.


for SimID in hpic_results/*
do
    start_file=$SimID/simulation-start
    end_file=$SimID/simulation-complete
    fail_file=$SimID/simulation-fail
    python3 parse_status_files.py $(hostname) $SimID $start_file $end_file $fail_file
 done

