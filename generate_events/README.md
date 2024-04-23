# Generation via MadGraph and Pythia using LCG

This process is still in its alpha testing stage.

## Set Up

1. Connect to LXPlus.

2. Source the LCG view 102b_ATLAS_6.

`source /cvmfs/sft.cern.ch/lcg/views/LCG_102b_ATLAS_6/x86_64-centos9-gcc11-opt/setup.sh`

3. Compile [main42.cc](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/generate_events/main42.cc) using prebuilt [script](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/generate_events/make_pythia_script.sh).

`bash make_pythia_script.sh`

`main42`

## Generation

If you ended your terminal session between setting up and beginning generation, repeat steps 1 and 2 above.

4. Run MadGraph, using [proc_card.dat](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/generate_events/proc_card.dat) as input.

`mg5_aMC proc_card.dat` 

5. Unzip the .lhe file produced by MadGraph.

`gunzip $PWD/PROC_RPVMSSM_UFO_0/Events/run_01/unweighted_events.lhe.gz`

6. Run [main42](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/generate_events/main42.cc), using [main42.cmnd](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/generate_events/main42.cmnd) as input. In the snippet below, the output data will be written to out.hepmc and the log file will be written to out.log.

`./main42 main42.cmnd out.hepmc > out.log`

# Initial Process for Generating Smuons with Mass = 400 GeV and Lifetime = 0.1 ns

Data sets used for testing other parts of this project were generated using the following process:

1. Follow instructions outlined [here](https://github.com/lawrenceleejr/DVMuReint#docker) to install Docker, pull the appropriate image, and import the required lhapdf sets.

2. Clone or download the [UFO model directory](https://github.com/lawrenceleejr/DVMuReint/tree/main/RPVMSSM_UFO).

3. From a directory that contains the UFO model, run the Docker image.

`docker run --rm -ti -v $PWD:$PWD -w $PWD scailfin/madgraph5-amc-nlo:mg5_amc3.3.1`

4. Run MadGraph, using [proc_card.dat](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/generate_events/proc_card.dat) as input.

`mg5_aMC proc_card.dat`

The process card does the following:

1. Imports the UFO model.

`import model /path/to/RPVMSSM_UFO/RPVMSSM_UFO/`

2. Instructs MadGraph not to create processes with quarks as mediators. We are interested in processes with the photon (a) and Z-boson (z) as mediators

`define q = g u c d s u~ c~ d~ s~ b t b~ t~ h01 h2 h3 h+ h-` 

3. Defines protons as multiparticles consisting of gluons, up, down, strange, charm, and bottom quarks/anti-quarks

`define p = g u c d s u~ c~ d~ s~ b b~`

4. Generates process

`generate p p > mur- mur+ /q`

5. Outputs preliminary files to a subdirectory automatically created in the location from which you ran MadGraph.

`output auto`

6. Launches the process.

`launch`

7. Turns on showering via Pythia.

`shower=Pythia8`

8. Changes the masses for both left- and right-handed smuons to 400 GeV. Both are necessary, as MadGraph expects them to match and will throw a fit if they don't.

`set mass 1000013 4.000000e+02`

`set mass 2000013 4.000000e+02`

9. Changes the decay width for right-handed smuons.

`set decay 2000013 6.500000e-15`

10. Changes the number of events to 20000.

`set nevents 20000`

11. Prevents MadGraph from interfering with the custom decay width (it will still fuss about it by throwing a warning during generation, which will show up in the debug log).

`set small_width_treatmean 1e-30`

# Troubleshooting and Sanity Checks

If you're unsure whether the generation process was completed appropriately, the output files include a directory called "Cards" that contains two very handy files: param_card.dat and run_card.dat. If your `set` commands functioned properly, they will have changed the following items:

In param_card.dat:

* Line 59 to:   1000013 4.000000e+02 # Msl2

* Line 77 to:   2000013 4.000000e+02 # Msl5

* Line 476 to:  DECAY 2000013 6.500000e-15 # Wsl5

In run_card.dat:

* Line 26 to: 20000 = nevents ! Number of unweighted events requested

* Final line to: 1e-30 = small_width_treatment
