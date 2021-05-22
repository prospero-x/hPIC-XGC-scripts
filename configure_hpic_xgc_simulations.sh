#!/usr/bin/env bash

### BEGIN USER MODIFICATION

# Path to hpic_1d3v executable installed on machine.
hpic_1d3v_path=/home/pc202/mikhail-hpic-runs/hPIC/hpic_1d3v/hpic

# XGC initial maxwellian dist
XGC_F0_MESH_BP=xgc.f0.mesh.bp

# XGC Bfield file
XGC_BFIELD_BP=xgc.bfield.bp

# XGC DIST BP
XGC_F0_XXXXX_BP=xgc.f0.00055.bp

# input file  CSV of format XGC_MESH_COORDINAGE,SURFACE_ANGLE
XGC_COORDS=xgc_coords.csv


# Hpic Params
output_directory=hpic_results
simulation_parent_id=xgc_d3d_sample_run

debye_lengths_in_domain=500
grid_points_per_debye_length=2
time_steps_per_gyroperiod=20
ion_acoustic_transit_times=10
particles_per_cell=20000

# Electric Potential BCs
BC_LEFT_VALUE=0
BC_RIGHT_VALUE=0

RF_wave_frequency=0  # rad/s
RF_Voltage_RIGHT=0   # V
RF_Voltage_LEFT=0    # V

kinfo=10  # number of times info is printed to stdout
kgrid=0   # numver of times griddata is saved
kpart=0   # number of times particledata is saved
kfluid=0  # number of times fluid data is saved


### END USER MODIFICATION

# evaluated fields
total_elems=$((debye_lengths_in_domain*grid_points_per_debye_length))


HPIC_COMMAND_TEMPLATE="${hpic_1d3v_path} -xgc SIMID $debye_lengths_in_domain
            $grid_points_per_debye_length $time_steps_per_gyroperiod
            $ion_acoustic_transit_times $particles_per_cell
            $BC_LEFT_VALUE $BC_RIGHT_VALUE $RF_wave_frequency $RF_Voltage_RIGHT
            $RF_Voltage_LEFT $kinfo $kgrid $kpart $kfluid 1 \"uniform\"
            \"$debye_lengths_in_domain\" \"$total_elems\" \"0\" $XGC_F0_MESH_BP
            $XGC_BFIELD_BP $XGC_F0_XXXXX_BP MESH_COORD THETA"


# For keeping track of simulation start and end times
DATE_FMT="+%Y-%m-%dT%H:%M:%S-%Z"

# Each simulation will have its own script.
scripts_dir="${simulation_parent_id}_scripts"
mkdir -p $scripts_dir

# Create a Parent script. This script will launch each simulation asynchronously
parent_script="launch_hpic_simulations_for_${simulation_parent_id}.sh"
echo "#!/usr/bin/env bash" > $parent_script
chmod 744 $parent_script

num_sims=0
for line in $(sed 1,1d $XGC_COORDS); do
    num_sims=$((num_sims + 1))

    mesh_coord=$(echo $line | cut -d, -f1)
    surface_theta=$(echo $line | cut -d, -f2)

    sim_id="${simulation_parent_id}_node_${mesh_coord}"

    # Each simulation takes place in its own directory, saving output there
    sim_dir=$output_directory/$sim_id
    mkdir -p $sim_dir

    # Make a link instead of copying the file because they can be large.
    if [ ! -f $sim_dir/$XGC_F0_MESH_BP ]; then
        ln $XGC_F0_MESH_BP    $sim_dir/$XGC_F0_MESH_BP
    fi
    if [ ! -f $sim_dir/$XGC_BFIELD_BP ];then
        ln $XGC_BFIELD_BP     $sim_dir/$XGC_BFIELD_B
    fi
    if [ ! -f $sim_dir/$XGC_F0_XXXXX_BP ];then
        ln $XGC_F0_XXXXX_BP   $sim_dir/$XGC_F0_XXXXX_BP
    fi

    sim_cmd=$(echo $HPIC_COMMAND_TEMPLATE \
        | sed "s/SIMID/$sim_id/g; \
               s/MESH_COORD/$mesh_coord/g; \
               s/THETA/$surface_theta/g")

    # write the command to a new bash scripti
    sim_script="${scripts_dir}/run_${sim_id}.sh"
    echo building $sim_script
    echo """#!/usr/bin/env bash
cd $sim_dir
date $DATE_FMT > simulation-start
eval $sim_cmd > hpic.log 2>hpic_errors.log

if [ \$? -eq 0 ]; then
    date $DATE_FMT > simulation-complete
else
    date $DATE_FMT > simulation-fail
fi""" > $sim_script

    chmod 744 $sim_script

    # Add this simulation script to the parent script runner. The script is
    # launched asynchronously
    echo """
echo starting hPIC 1d3v simulation for $sim_id...
$sim_script &""" >> $parent_script
done


echo """

echo Started $num_sims simulations.
echo Run check_status.sh to view the status of each simulation." >> $parent_script

echo
echo building parent script: $parent_script
