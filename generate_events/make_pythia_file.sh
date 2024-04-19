#!/bin/bash
cd /cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/310-2f242/x86_64-el9-gcc13-opt/share/Pythia8/examples/
/cvmfs/sft.cern.ch/lcg/releases/gcc/13.1.0-b3d18/x86_64-el9/bin/g++ \
	/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main42.cc \
	-o /eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main42 \
	-I /cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/310-2f242/x86_64-el9-gcc13-opt/include \
	-O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC -pthread -DGZIP -lz \
	-L/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/310-2f242/x86_64-el9-gcc13-opt/lib \
	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/310-2f242/x86_64-el9-gcc13-opt/lib\
	-lpythia8 -ldl \
	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc13-opt/lib \
	-llibHepMC
cd -
