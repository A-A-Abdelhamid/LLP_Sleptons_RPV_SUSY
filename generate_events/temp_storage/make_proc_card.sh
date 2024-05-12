#!/bin/bash

# --- Header --- #
nevents=$1

mass_start=$2
mass_end=$3
mass_increment=$4
mass=$mass_start

# This section is mostly a placeholder. Decay range coming soon.
lifetime_start=$5
lifetime_end=$6
lifetime_increment=$7
lifetime=$lifetime_start

model_dir=$8
proc_card_name=$9

run_dir='smu'$mass'gev'$lifetime'ns'
# --- End of Header --- #

touch $proc_card_name
echo import model $model_dir > $proc_card_name
echo define q = g u c d s u~ c~ d~ s~ b t b~ t~ h01 h2 h3 h+ h- >> $proc_card_name
echo define p = g u c d s u~ c~ d~ s~ b b~ >> $proc_card_name
echo 'generate p p > mur- mur+ /q' >> $proc_card_name
echo output auto >> $proc_card_name
echo launch -n $run_dir >> $proc_card_name
echo ./param_card_default.dat >> $proc_card_name
echo set nevents $nevents >> $proc_card_name
echo set time_of_flight 0.0 >> $proc_card_name
echo set small_width_treatment 1e-30 >> $proc_card_name
echo set mass 1000013 $mass >> $proc_card_name
echo set mass 2000013 $mass >> $proc_card_name
echo set decay 2000013 6.500000e-15 >> $proc_card_name

#TODO Add decay range functionality
for ((mass=$mass_start+100;mass<=mass_end;mass=$mass+100)); do
	run_dir='smu'$mass'gev'$lifetime'ns'
	echo launch -n $run_dir >> $proc_card_name
	echo set mass 1000013 $mass >> $proc_card_name
	echo set mass 2000013 $mass >> $proc_card_name
	echo set decay 2000013 6.500000e-15 >> $proc_card_name
done

echo done >> $proc_card_name
