import os
import pyhepmc
from pyhepmc.view import savefig

hepmc_file = "../../run_data/run_17/Events/run_01/tag_1_pythia8_events.hepmc"

output_dir = "event_diagrams"
# NOTE ↓ This will refer to the path from which this script **executed**
parent_path = os.getcwd() 

full_path = os.path.join(parent_path, output_dir)
os.mkdir(full_path)

with pyhepmc.open(hepmc_file) as f:
    # Loop over events in the file
    for i, event in enumerate(f):
        # Save a plot of the event
        savefig(event, f"{output_dir}/event{i}.svg")
        savefig(event, f"{output_dir}/event{i}.pdf")

