#!/bin/bash

# --- Header --- #
nevents=3
model_repo='https://github.com/lawrenceleejr/DVMuReint.git'
model_dir="$PWD/DVMuReint/RPVMSSM_UFO/RPVMSSM_UFO/"

mass_start=300
mass_end=500
mass_increment=100
mass=$mass_start

lifetime_start=1
lifetime_end=1
lifetime_increment=1
lifetime=$lifetime_start

run_dir='smu'$mass'gev'$lifetime'ns'

mg_dir_name='PROC_RPVMSSM_UFO_'
mg_dir_i=0
mg_dir=$mg_dir_name$mg_dir_i

proc_card_name='auto_proc_card.dat'
# --- End of Header --- #

source /cvmfs/sft.cern.ch/lcg/views/LCG_102b_ATLAS_6/x86_64-centos9-gcc11-opt/setup.sh

echo LCG sourced. Cloning model from $model_repo.
git clone $model_repo

echo Cloning complete. Creating $proc_card_name with
printf '%s\n' "	Inital mass     = $mass_start GeV"
printf '%s\n' "	Final mass      = $mass_end GeV"
printf '%s\n' "	Inital lifetime = $lifetime ns"
printf '%s\n' "	Final lifetime  = $lifetime ns"
mass_dirs=$(( ( mass_end - mass_start ) / mass_increment + 1 ))
lifetime_dirs=$(( ( lifetime_end - lifetime_start ) / lifetime_increment + 1 ))
total_dirs=$(( mass_dirs * lifetime_dirs ))
total_events=$(( total_dirs * nevents ))
echo with $nevents events each for a total of $total_dirs directories and $total_events events.

bash make_proc_card.sh $nevents $mass_start $mass_end $mass_increment $lifetime_start $lifetime_end $lifetime_increment $model_dir $proc_card_name

echo Running MadGraph with $proc_card_name.
mg5_aMC $proc_card_name > mg5.log

echo MadGraph generation completed. See mg5.log for more info.
echo Starting hadroniztion in the following directories:
ls $PWD/$mg_dir/Events

for ((mass=$mass;mass<=mass_end;mass=$mass+100)); do
       	run_dir='smu'$mass'gev'$lifetime'ns'
	full_run_dir=$PWD/$mg_dir/Events/$run_dir
       	gunzip $full_run_dir/unweighted_events.lhe.gz
	echo $run_dir LHEF unzipped.
	cp main42.cmnd $full_run_dir/main42.cmnd
	sed -i "s|Beams:LHEF = /path/to/LHEF/f.lhe   ! the LHEF to read from|Beams:LHEF = $PWD/$mg_dir/Events/$run_dir/unweighted_events.lhe|" $full_run_dir/main42.cmnd
	sed -i "s|Main:numberOfEvents = 3|Main:numberOfEvents = $nevents|" $full_run_dir/main42.cmnd
	./main42 $full_run_dir/main42.cmnd $full_run_dir/out.hepmc > $full_run_dir/out_$run_dir.log
	echo Hadronization complete for $run_dir.
done

echo Full generation process done.
