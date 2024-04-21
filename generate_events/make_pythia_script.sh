#!/bin/bash
# To use, replace the file names at the end of lines 8 and 10 with your file name.
# If compiling a script for HepMC output, uncomment the last 5 lines.

# Run compiler
/cvmfs/sft.cern.ch/lcg/releases/gcc/11.3.0-ad0f5/x86_64-centos9/bin/g++ \
	# Pass path for to-be-compiled file to compiler
	/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main38.cc \
	# Specify output
	-o /eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main38 \
	# Reference the Pythia default configuration files
	-I/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/include \
	# Include Pythia's default flags
	-O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC -pthread -DGZIP -lz \
	# Reference the primary Pythia libraries
	-L/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/lib \
	# Specifically look for pythia8.so
	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/lib \
	-lpythia8 -ldl \
	# Repeat the process from lines 15-19 for HepMC
#	-I/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/include \
#	-L/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib \
#	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib \
#	-lHepMC\
# -DHEPMC2
