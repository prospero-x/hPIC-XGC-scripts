import sys, os
from datetime import datetime

# This script is meant to be run DURING hPIC simulations, in order
# to see which hPIC simulations are complete and which ones are still running.
# It's meant to be a more accurate representation than "$htop" or
# "$ ps -ef | grep hpic | grep <MY_SIMULATION_PATTERNS>".
#
# It assumes that, before a particular hPIC simulation, a file named
# "simulation-start" was created in the particular hPIC simualtion subdirectory,
# containing a single line date time string in the format %Y-%m-%dT%H:%S-%Z.
# Similarlty, it assumes that ones an hPIC simulation is complete, a similar
# file named "simulation-complete" is created.
#
# Finally, the assumption is that, if the hpic simulation exited with a nonzero
# exit code, a file called "simulation-fail" was created containing a date value.


DEFAULT_DATE = datetime(1970,1,1,0,0,0)
start = end = fail = DEFAULT_DATE
now = datetime.now()

DATE_FMT="%Y-%m-%dT%H:%M:%S-%Z"

hostname = sys.argv[1]
SimID = sys.argv[2].split("hpic_results/")[1]
if len(sys.argv) < 4:
    print(f"{hostname}: {SimID:35} not started!")
    sys.exit(0)

#
# Parse "simulation-start" file
#
startfile = sys.argv[3]
if not os.path.exists(startfile):
    print(f"WARNING: \"{startfile}\" does not exist. Cannot check status of this"
         + " simulation.")
    sys.exit(1)

with open(startfile, "r") as f:
    val = f.readline().strip()
    try:
        start = datetime.strptime(val, DATE_FMT)
    except Exception as e:
        print(f"ERROR: found invalid date in {startfile}: Line 1: \"{val}\"")
        sys.exit(1)

#
# Parse "simulation-end" file. OK if this file does not exist.
#
endfile = sys.argv[4]
if os.path.exists(endfile):
    with open(endfile, "r") as f:
        val = f.readline().strip()
        try:
            end = datetime.strptime(val, DATE_FMT)
        except Exception as e:
            print(f"ERROR: found invalid date in {endfile}: Line 1: \"{val}\"")
            sys.exit(1)

#
# Parse "simulation-fail" file. OK if thie file does not exist.
#
failfile = sys.argv[5]
terminated = False
if os.path.exists(failfile):
    with open(failfile, "r") as f:
        val = f.readline().strip()
        try:
            fail = datetime.strptime(val, DATE_FMT)
        except Exception as e:
            print(f"ERROR: found invalid date in {failfile}: Line 1: \"{val}\"")
            sys.exit(1)

if end >= start:
    print(f"{hostname}: {SimID:35} done (took {end - start})")
elif fail >= start:
    # read hpic_error.log to see if the simulation was terminated by a
    # user or failed unexpectedly
    errors_log_file = f'hpic_results/{SimID}/hpic_errors.log'
    if os.path.exists(errors_log_file):
        f = open(errors_log_file, "r")
        contents = f.read().strip()
        f.close()
        if contents == 'Terminated':
            print(f"{hostname}: {SimID:35} terminated by user.")
        else:
            print(f"{hostname}: {SimID:35} failed! Check hpic_error.log for details.")
    else:
            print(f"{hostname}: {SimID:35} failed! Could not find hpic_error.log file.")
else:
    print(f"{hostname}: {SimID:35} still running (running for {now - start})")

