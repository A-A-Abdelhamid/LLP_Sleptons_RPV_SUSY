import pyhepmc
from pyhepmc.view import savefig

filename = "../../run_data/run_17/Events/run_01/tag_1_pythia8_events.hepmc"
# pyhepmc.open can read most HepMC formats using auto-detection
with pyhepmc.open(filename) as f:
    # Loop over events in the file
    for i, event in enumerate(f):
        # Save a plot of the event
        savefig(event, f"event{i}.svg")
        savefig(event, f"event{i}.png")
        savefig(event, f"event{i}.pdf")




   

      

