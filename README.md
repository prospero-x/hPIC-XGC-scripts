# hPIC-with-XGC helper scripts

These scripts are meant to facilitate the execution, tracking, and monitoring of hPIC simulations launced with XGC input. 
[hPIC](https://www.sciencedirect.com/science/article/abs/pii/S0010465518301012?via%3Dihub) is a hybrid Particle-in-Cell plasma simulation code written at LCPP at University of Illinois at Urbana-Champaign. XGC is a gyrokinetic plasma. [XGC](https://hbps.pppl.gov/computing/xgc-1) is a gyrokinetic particle-in-cell code written at Princeton Plasma Physics Laboratory. This code is meant to be run after XGC simulations. It configures hPIC simulations to be run for each node of interest in the XGC messh.

### Requirements:
The output of a completed XGC simulation, including a`xgc.f0.mesh.bp`, `xgc.bfield.bp`, and `xgc.f0.#####.bp`, where `#####` represents the time step. The hPIC simulation will be configured based on the distribution found in `xgc.f0.#####.bp`.

### Step 1: Choose XGC Nodes
Visually inspect the XGC mesh and select individual nodes of interest. One hPIC simulation will be run for each node of interest. In addition, determine the poloidal angle of the surface close to the node you are choosing. theta = 0 represents the D3D divertor (pointing in the +z direction), while +90 indicates a surface pointing in the +R direction, and -90 indicates a surface pointing in the -R direction.

### Step 2: Save Nodes to File
Save the mesh coordinates and angles to a CSV file, for example `xgc_nodes.csv`. The format of the file must be:
```
MESH_NODE,SURFACE_ANGLE
6000,0
12345,22.4
36803,11
```

The first line of this file **must** contain column names (they can be called anything)

### Step 3: Configure hPIC simulations
Update all bash fields in `configure_hpic_xgc_simulations.sh` between the lines `### BEGIN USER MODIFICATION` and `### END USER MODIFICATION`. For a further
explanation of fields, run `./hpic -xgc` to see a print-out of field descriptions.

Once you have modified `configure_hpic_xgc_simulations.sh` to your liking, run:
```bash
./configure_hpic_xgc_simulations.sh xgc.f0.mesh.bp xgc.bfield.bp xgc.f0.#####.bp xgc_nodes.csv 
```

This will create the following:
`launch_hpic_simulations_for_<PARENT_SIMULATION_ID>.sh`: the parent bash script to launch all simulations. Executing this script will launch one hpic simulation, asynchronously, for each (`node_id`, `surface_theta`) pair in `xgc_nodes.csv`
`<PARENT_SIMULATION_ID>_run_scripts`: a directory containing one bash script for each hPIC simulation to be run. One script will be created for each line in `xgc_nodes.csv`
`hpic_results`: a directory containing one subdirectory for each line in `xgc_nodes.csv`. Simulations will be run in each subdirectory, and output will be saved here.

### Step 4: Launch simulations
Run the following command to launch one hpic simulation, asynchronously, for each line in `xgc_nodes.csv`:
```bash
launch_hpic_simulations_for_<PARENT_SIMULATION_ID>.sh
```

### Step 5: Monitor Simulations
To monitor simulations, run:
```bash
./check_status.sh
```

### Step 6 (Optional): Kill Simulations
To kill all simulations launched in step 4, modify `kill_simulations.sh` and set `parent_simulation_id` to the same value as was used to configure simulations. Then save and execute the script. All simulations will be killed. Note running `./check_status.sh` after this step will display failures for each hPIC simulation.

