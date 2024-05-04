#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_102b_ATLAS_6/x86_64-centos9-gcc11-opt/setup.sh
cp /cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/share/Pythia8/examples/main42.cc main42.cc
bash make_pythia_script.sh main42
