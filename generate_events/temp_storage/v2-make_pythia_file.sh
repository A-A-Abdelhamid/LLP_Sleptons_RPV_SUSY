/cvmfs/sft.cern.ch/lcg/releases/gcc/11.3.0-ad0f5/x86_64-centos9/bin/g++ \
	/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main38.cc \
	-o /eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/main38 \
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