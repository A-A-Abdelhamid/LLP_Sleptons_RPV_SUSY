import pyhepmc
from pyhepmc.view import savefig

filename = "tag_1_pythia8_events.hepmc"
# pyhepmc.open can read most HepMC formats using auto-detection
with pyhepmc.open(filename) as f:
    # Loop over events in the file
    for i, event in enumerate(f):
        # Save a plot of the event
        if event.event_number == 868 or i ==868:
          savefig(event, f"event{i}.svg")
          savefig(event, f"event{i}.png")
          savefig(event, f"event{i}.pdf")
          for particle in event.particles:
            if particle.id ==552 and particle.pid==-211:
              ver=particle.production_vertex
              print(ver)
              print("i: ",i, "    event#:   ", event.event_number)



   

      

