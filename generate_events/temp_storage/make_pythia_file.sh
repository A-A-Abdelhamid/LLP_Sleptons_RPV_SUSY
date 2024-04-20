#!/bin/bash
cd $PYTHIA8/share/Pythia8/examples/
$CXX \
	/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main01.cc \
	-o /eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main01 \
	-I $PYTHIA8/include \
	-O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC -pthread -DGZIP -lz \
#	-l/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/include \
#	-L/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib 
#	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib -llibHepMC
	-L$PYTHIA8/lib \
	-Wl,-rpath,$PYTHIA8/lib\
	-lpythia8 -ldl 
cd -
