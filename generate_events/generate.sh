#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_102b_ATLAS_6/x86_64-centos9-gcc11-opt/setup.sh
mg5_aMC proc_card.dat
gunzip $PWD/PROC_RPVMSSM_UFO_0/Events/run01/unweighted_events.lhe.gz
./main42 main42.cmnd out.hepmc > out.log
