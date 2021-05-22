#!/usr/bin/env bash

LCPP_HOSTS_FILE=lcpp_hosts.txt
# Ignore #-style comments and blank lines
lcpp_hosts=$(grep -Ev '^$|#.*' $LCPP_HOSTS_FILE)

# For each LCPP host, SCP all local scripts intended to be run on that host
# to that host. Destination dir must already exist on remote host.
#
# Example: ./send_files_to_all_hosts.sh mikhail-hpic-run


REMOTE_DEST_DIR="$1"

if [ -z $REMOTE_DEST_DIR ]; then
    echo usage: ./send_files_to_all_hosts.sh \<DESTINATION_DIRECTORY\>
    exit 1
fi

_SEND_TO_ALL=(
    check_status.sh
    parse_status_files.py
    kill_simulations.sh
    configure_hpic_xgc_simulations.sh
    xgc_coords.csv
    send_results_to_mikhail.sh
    #xgc.f0.mesh.bp
    #xgc.bfield.bp
    #xgc.f0.00055.bp
)


for host in $lcpp_hosts; do
    for file in ${_SEND_TO_ALL[*]}; do
        scp $file $host:$REMOTE_DEST_DIR
    done
done
