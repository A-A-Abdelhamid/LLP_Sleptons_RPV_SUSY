#!/bin/bash
# If compiling a script that does not require HepMC output, 
# comment out the last 5 lines.

# Line-by-line breakdown:
# 13) Set filename from argument; 15) run compiler; 
# 16) pass path for to-be-compiled file to compiler; 
# 17) specify output; 18) reference Pythia default config files;
# 19) include Pythia default flags; 20) reference Pythia libraries;
# 21-22) specifically look for pythia8.so;
# 23-26) repeat the process from lines 20-22 for HepMC; 27) ???

filename=$1

$CXX \
	$PWD/$filename.cc \
	-o $PWD/$filename \
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
