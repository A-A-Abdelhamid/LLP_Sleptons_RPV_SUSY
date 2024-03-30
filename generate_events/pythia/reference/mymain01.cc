#include "Pythia8/Pythia.h"
#include "Pythia8Plugins/HepMC3.h"

using namespace Pythia8;

int main() {
	string lhe_file = "unweighted_events.lhe";
	// Interface for conversion from Pythia8::Event to HepMC
	// event. Specify file where HepMC events will be stored.
	HepMC3::Pythia8ToHepMC toHepMC(lhe_file);
	
	// Generator. Process selection. LHC initialization. Histogram.
	Pythia pythia;
	
	// Initialize Les Houches Event File run. List initialization information.
	pythia.readString("Beams:frameType = 4");
	pythia.readString("Beams:LHEF = " + lhe_file);
	
	pythia.init();

	// Allow for possibility of a few faulty events.
	int nAbort = 10;
	int iAbort = 0;
	
	// Begin event loop; generate until none left in input file.
	while (iAbort < nAbort) {
		// Generate events, and check whether generation failed.
		if (!pythia.next()) {
			// If failure because reached end of file then exit event loop.
			if (pythia.info.atEndOfFile()) break;
			++iAbort;
			continue;
		}
	}

	// Construct new empty HepMC event, fill it and write it out.
	toHepMC.writeNextEvent( pythia );

	// End of event loop. Statistics.
	pythia.stat();

	// Done.
	return 0;
}
