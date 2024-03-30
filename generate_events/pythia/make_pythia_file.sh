#!/bin/bash
cd /cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/310-2f242/x86_64-el9-gcc13-opt/share/Pythia8/examples/
echo Enter file name, excluding extensions such as .cc:
read to_be_compiled
make /eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/pythia/$to_be_compiled 
cd -
