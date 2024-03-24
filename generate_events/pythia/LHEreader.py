# Based off of main01.py, main11.cc, and main41.cc, all parts of the PYTHIA event generator.
# Copyright (C) 2024 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.

# Import the Pythia module.
import pythia8
import pyhepmc
pythia = pythia8.Pythia()

# Name of LHE file
data = 'unweighted_events.lhe'

# Beam and event info is in LHE file
pythia.readString("Beams:frameType = 4")
# Pythia directions to LHE file
pythia.readString(f"Beams:LHEF = {data}")

pythia.init()

# Error checking
nAbort = 10
iAbort = 0

# Begin event loop; generate until end of input file
while iAbort < nAbort:
    if not pythia.next(): 
        # TODO This fails. Need to fix.
        # If fail, check for end
        if pythia.info.atEndOfFile():
            break 
        # If not end, tally error
        iAbort += 1
        continue

# TODO This is broken. I'll poke at fixing it at some point. Maybe.
# Output
#pyhepmc.Pythia8ToHepMC3( toHepMC('hepmcout.dat') )
#toHepMC.writeNextEvent(pythia)

# End of event loop. Statistics. Histogram. Done.
pythia.stat();
