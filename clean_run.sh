#!bin/bash
data_path=$PWD/../run_data

ls $data_path
echo Enter run number
read runnum

new_data_path=$data_path/run_$runnum

mkdir $new_data_path

mv $PWD/analysis/expected.pdf $new_data_path
mv $PWD/event_validation/event1.pdf $new_data_path
mv $PWD/event_validation/event1.png $new_data_path
mv $PWD/event_validation/event1.svg $new_data_path
mv $PWD/event_validation/muon_eta.png $new_data_path
mv $PWD/event_validation/muon_phi.png $new_data_path
mv $PWD/event_validation/muon_pT.png $new_data_path
mv $PWD/generate_events/out.hepmc $new_data_path
mv $PWD/generate_events/out.log $new_data_path

