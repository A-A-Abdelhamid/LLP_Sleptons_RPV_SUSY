#!/bin/bash

# --- Header --- #
nevents=20000
pythia_filename='main42'
model_repo='https://github.com/lawrenceleejr/DVMuReint.git'
model_dir="$PWD/DVMuReint/RPVMSSM_UFO/RPVMSSM_UFO/"

mass=$1
lifetime=$2

hbar="$( awk 'BEGIN {print ( 6.582119569 * (10^-16) ) }' )"
decay="$( awk 'BEGIN {print ($hbar / $lifetime) }')"

run_dir='smu'$mass'gev_'$lifetime'ns'

proc_card_name='auto_proc_card.dat'
output_dir='/eos/user/j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/data'
# --- End of Header --- #

source /cvmfs/sft.cern.ch/lcg/views/LCG_102b_ATLAS_6/x86_64-centos9-gcc11-opt/setup.sh
echo LCG sourced. Compiling Pythia script.

# --- Pythia Script Compilation --- #
$CXX \
        $PWD/$pythia_filename.cc \
        -o $PWD/$pythia_filename \
        -I$PYTHIA8/include \
        -O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC -pthread -DGZIP -lz \
        -L$PYTHIA8/lib \
        -Wl,-rpath,$PYTHIA8/lib \
        -lpythia8 -ldl \
        -I/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/include \
        -L/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib \
        -Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib \
        -lHepMC\
 -DHEPMC2
# --- End of Pythia Script Compilation --- #

echo Cloning model from $model_repo.
git clone $model_repo

echo Cloning complete. Model directory contents:
ls $model_dir

echo Creating $proc_card_name for process with
printf '%s\n' "	Mass     = $mass GeV"
printf '%s\n' "	Lifetime = $lifetime ns"

# --- Process Card Creation --- #
touch $proc_card_name
echo import model $model_dir > $proc_card_name
echo define q = g u c d s u~ c~ d~ s~ b t b~ t~ h01 h2 h3 h+ h- >> $proc_card_name
echo define p = g u c d s u~ c~ d~ s~ b b~ >> $proc_card_name
echo 'generate p p > mur- mur+ /q' >> $proc_card_name
echo output $run_dir >> $proc_card_name
echo launch >> $proc_card_name
echo ./param_card_default.dat >> $proc_card_name
echo set nevents $nevents >> $proc_card_name
echo set time_of_flight 0.0 >> $proc_card_name
echo set small_width_treatment 1e-30 >> $proc_card_name
echo set mass 1000013 $mass >> $proc_card_name
echo set mass 2000013 $mass >> $proc_card_name
echo set decay 2000013 $decay >> $proc_card_name
echo done >> $proc_card_name
# --- End of Process Card Creation --- #

echo Running MadGraph with $proc_card_name.
mg5_aMC $proc_card_name > mg5.log

echo MadGraph generation completed. See mg5.log for more info.
echo Starting hadroniztion in the following directories:
ls $PWD/$run_dir/Events

# --- LHEF Processing --- #
full_run_dir=$PWD/$run_dir/Events/run_01
gunzip $full_run_dir/unweighted_events.lhe.gz
echo $run_dir LHEF unzipped.
cp main42.cmnd $full_run_dir/main42.cmnd
sed -i "s|Beams:LHEF = /path/to/LHEF/f.lhe   ! the LHEF to read from|Beams:LHEF = $full_run_dir/unweighted_events.lhe|" $full_run_dir/main42.cmnd
sed -i "s|Main:numberOfEvents = 3|Main:numberOfEvents = $nevents|" $full_run_dir/main42.cmnd
./main42 $full_run_dir/main42.cmnd $full_run_dir/out.hepmc > $full_run_dir/out_$run_dir.log
echo Hadronization complete for $run_dir.
# --- End of LHEF Processing --- #

echo Full generation process done.

echo Compressing and copying output to EOS.

# --- Stage-Out --- #
echo Files to be copied:
ls $full_run_dir

tar -czf output.tgz $full_run_dir/*

export EOS_MGM_URL=root://eosuser.cern.ch

eos cp -p output.tgz $output_dir/$run_dir/

echo "Files compressed and copied to $output_dir/$run_dir. Contents:"
ls $output_dir/$run_dir
# --- End of Stage-Out --- #
