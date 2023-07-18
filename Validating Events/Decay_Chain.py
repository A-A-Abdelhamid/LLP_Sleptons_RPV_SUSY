import pyhepmc
import ROOT
from collections import Counter

def get_decay_products(particle, event_num):
    """
    Get the decay products of a given particle.
    """
    proper_decay_products = []
    other_particles = []

    # Check if the particle itself is a final state muon or neutrino
    if particle.status == 1 and abs(particle.pid) in [13, 12, -13, -12]:
        proper_decay_products.append((particle.pid, particle.id))
    elif particle.status == 1:
        other_particles.append((particle.pid, particle.id, event_num))
    # If the particle has an end vertex, check its descendants recursively
    if particle.end_vertex:
        for p in particle.end_vertex.particles_out:
            proper, other = get_decay_products(p, event_num)
            proper_decay_products.extend(proper)
            other_particles.extend(other)
    return proper_decay_products, other_particles

def track_decay_chain(hepmc_file):
    """
    Track the decay chain of muons and neutrinos that originate from a particle with abs pid 2000013.
    """
    proper_decay_products = []
    other_particles = []

    # Open the HepMC file
    with pyhepmc.open(hepmc_file) as f:
        # Loop over events in the file
        for i, event in enumerate(f):
            # Loop over particles in the event
            for particle in event.particles:
                # Check if the particle is a muon or neutrino produced by a decaying 2000013 or -2000013
                if particle.production_vertex and any(p.pid in [2000013, -2000013] for p in particle.production_vertex.particles_in):
                    # Get the decay products of the particle
                    proper, other = get_decay_products(particle, i)
                    proper_decay_products.extend(proper)
                    other_particles.extend(other)

    # Count the frequencies of each particle PID
    proper_decay_counter = Counter([pid for pid, _ in proper_decay_products])
    other_particles_counter = Counter([pid for pid, _, _ in other_particles])

    # Find the first non-22 PID in other_particles
    first_non_22 = next((pid, id, event_num) for pid, id, event_num in other_particles if pid != 22)

    print("Proper decay products:", proper_decay_counter)
    print("Other particles:", other_particles_counter)
    print("First non-22 PID in 'other_particles': PID = {}, ID = {}, Event number = {}".format(*first_non_22))

# Use the function
track_decay_chain('tag_1_pythia8_events.hepmc')
