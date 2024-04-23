import pyhepmc
from pyhepmc.view import savefig

filename = "/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/out.hepmc"

event_num = 1 # Event number to plot
p_id = 1399 # Particle index number in record
p_pid = -211 # PDG ID of particle

with pyhepmc.open(filename) as f:
    # Loop over events in the file
    for i, event in enumerate(f):
        # Save a plot of the event
        if event.event_number == event_num or i == event_num:
          savefig(event, f"event{i}.svg")
          savefig(event, f"event{i}.png")
          savefig(event, f"event{i}.pdf")
          for particle in event.particles:
            if particle.id == p_id and particle.pid == p_pid:
              ver = particle.production_vertex
              print(ver)
              print("i: ",i, "    event#:   ", event.event_number)

