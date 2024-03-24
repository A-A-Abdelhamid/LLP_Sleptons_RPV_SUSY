import numpy as np
import pyhepmc as hep
import yaml

# --- CSV ---
og_file = "HEPData-ins1831504-v2-Smuon_acceptance.csv"
np_og_data = np.genfromtxt(og_file, delimiter=',')
og_data = np.ndarray.tolist(np_og_data)

# Removes header line from numpy array
del(og_data[0])

# --- YAML ---
#og_file = "HEPData-ins1831504-v2-Smuon_acceptance.yaml"
#with open(og_file, 'r') as f:
#    og_data = yaml.load(f, Loader=yaml.SafeLoader) 

#acceptance = og_data.get('dependent_variables', {})[0].get('values')

#TODO All this section should be read in from RESULTS file
sparticle_mass = 400 #GeV
sparticle_lifetime = 0 #log_10(ns)
sparticle_acceptance = 0
uncertainty = 0

mass_bin = 0
lifetime_bin = 0
og_acceptance = 0

for row in og_data:
    if sparticle_mass <= row[0]:
        mass_bin = row[0]
        if sparticle_lifetime <= row[1]:
            lifetime_bin = row[1]
            og_acceptance = row[2]
            break

print('Mass bin =', mass_bin)
print('Lifetime bin =', lifetime_bin)
print('Acceptance in original paper =', og_acceptance)
