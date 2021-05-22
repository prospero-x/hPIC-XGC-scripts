#!/usr/bin/env bash

# This script is used to kill all hpic_1d3v simulations whose simulation IDs
# match a pattern. The pattern approach ensures that other hpic simulations
# running on the same box are not stopped.:

simulation_parent_id="xgc_d3d_sample_run"

ps -ef | grep "hpic -xgc ${simulation_parent_id}" | head -n -1 | awk '{print $2}' | xargs kill

