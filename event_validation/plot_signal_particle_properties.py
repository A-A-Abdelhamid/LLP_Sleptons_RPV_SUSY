import pyhepmc
import matplotlib.pyplot as plt
import numpy as np

# CHANGE ME :)
hepmc_file = "/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/generate_events/out.hepmc"
signal_pid = 13                    # signal particle id
signal_particle = 'muon'           # signal particle name (for labeling)
signal_parent = 2000013            # id of parent of signal particle

pos_particle_pts = []
pos_particle_etas = []
pos_particle_phis = []

neg_particle_pts = []
neg_particle_etas = []
neg_particle_phis = []

# Check particle for potential as a signal
def has_signal_parent(particle):
    if abs(particle.pid) == signal_pid and particle.production_vertex:
        if any(p.pid in [signal_parent, -signal_parent] for p in particle.production_vertex.particles_in):
            return True
    return False

# Get final state particles
def get_signal(particle):
    # Check if the particle itself is a signal particle
    if particle.status == 1 and abs(particle.pid) == signal_pid:
        return particle
    # If the particle has an end vertex, check its descendants recursively
    elif particle.end_vertex and abs(particle.pid) == signal_pid:
        for p in particle.end_vertex.particles_out:
            final_particle = get_signal(p)
            if final_particle is not None:
                return final_particle
    # If the particle is not a final state particle and does not have an end vertex, return None
    return None

def mev_to_gev(mev):				# pT values are in MeV,
	return mev * 10**-3			    # converting to GeV

num_particles = 0

with pyhepmc.open(hepmc_file) as f:
    for event in f:
        for particle in event.particles:
            # Check if the particle is produced by a decaying 2000013 or -2000013
            if has_signal_parent(particle):
            # Get the final descendant of the signal particle
                signal_particle = get_signal(particle)
                if signal_particle is not None:
                    if particle.pid == signal_pid:
                        num_particles += 1
                        p_pt = mev_to_gev( particle.momentum.pt() )
                        pos_particle_pts.append(p_pt)
                        p_eta = particle.momentum.eta()
                        pos_particle_etas.append(p_eta)
                        p_phi = particle.momentum.phi()
                        pos_particle_phis.append(p_phi)
                    elif particle.pid == -signal_pid:
                        num_particles += 1
                        n_pt = mev_to_gev( particle.momentum.pt() )
                        neg_particle_pts.append(n_pt)
                        n_eta = particle.momentum.eta()
                        neg_particle_etas.append(n_eta)
                        n_phi = particle.momentum.phi()
                        neg_particle_phis.append(n_phi)

# HISTOGRAM STUFF
tags = [f'Positively charged {signal_particle}s', f'Negatively charged {signal_particle}s']

# --- pT ---
pTs = [pos_particle_pts, neg_particle_pts]

pT_num_bins = np.linspace(0, 3000, 50)

plt.hist(pTs, bins=pT_num_bins, histtype='bar', label=tags, stacked=True, edgecolor='black')

plt.xlabel('pT [GeV]')
plt.ylabel(f'number of {signal_particle}s')
plt.title(f'{signal_particle} pT')

plt.legend()
plt.grid(color='c')

plt.savefig(f'{signal_particle}_pT.png', bbox_inches='tight')
plt.clf()

# --- eta ---
etas = [pos_particle_etas, neg_particle_etas]
eta_extrema = max (np.abs( np.min(etas) ), np.max(etas) )
eta_num_bins = np.linspace( -5, 5 )

plt.hist(etas, bins=eta_num_bins, histtype='bar', label=tags, stacked=True, edgecolor='black')

plt.xlabel('$\eta$')
plt.ylabel(f'number of {signal_particle}s')
plt.title(f'{signal_particle} $\eta$')

plt.legend()
plt.grid(color='c')

plt.savefig(f'{signal_particle}_eta.png', bbox_inches='tight')
plt.clf()

# --- phi ---
phis = [pos_particle_phis, neg_particle_phis]

phi_num_bins = np.linspace( -np.pi, np.pi, 32 )

plt.hist(phis, bins=phi_num_bins, histtype='bar', label=tags, stacked=True, edgecolor='black')

plt.xlabel('$\phi$')
plt.ylabel(f'number of {signal_particle}s')
plt.title(f'{signal_particle} $\phi$')

plt.legend()
plt.grid(color='c')

plt.savefig(f'{signal_particle}_phi.png', bbox_inches='tight')

# --- misc ---
print(num_particles,f'{signal_particle}s generated')
print(np.max(pTs),'max pT')
print(eta_extrema,'eta extremum')
print(np.sum(phis) / num_particles,'average phi')
