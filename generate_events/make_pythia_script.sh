#!/bin/bash
# TO USE: replace the file names at the end of lines 8 and 10 with your file name.
# If compiling a script for HepMC output, uncomment the last 5 lines.

# 11) Run compiler; 12) pass path for to-be-compiled file to compiler; 
# 13) specify output; 14) reference Pythia default config files;
# 15) include Pythia default flags; 16) Reference Pythia libraries;
# 17-18) specifically look for pythia8.so;
# 19-23) repeat the process from lines 14-18 for HepMC

echo Enter file name, excluding the extension:
read filename

/cvmfs/sft.cern.ch/lcg/releases/gcc/11.3.0-ad0f5/x86_64-centos9/bin/g++ \
	/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/$filename.cc \
	-o /eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/$filename \
	-I/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/include \
	-O2 -std=c++11 -pedantic -W -Wall -Wshadow -fPIC -pthread -DGZIP -lz \
	-L/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/lib \
	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/MCGenerators/pythia8/308-3f34f/x86_64-centos9-gcc11-opt/lib \
	-lpythia8 -ldl \
#	-I/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/include \
#	-L/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib \
#	-Wl,-rpath,/cvmfs/sft.cern.ch/lcg/releases/HepMC/2.06.11-d5a39/x86_64-centos9-gcc11-opt/lib \
#	-lHepMC\
# -DHEPMC2
