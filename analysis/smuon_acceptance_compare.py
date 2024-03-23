import numpy as np
import pyhepmc as hep
import yaml

# --- CSV ---
#og_file = "HEPData-ins1831504-v2-Smuon_acceptance.csv"
#og_data = np.genfromtxt(og_file, delimiter=',')

# --- YAML ---
og_file = "HEPData-ins1831504-v2-Smuon_acceptance.yaml"
with open(og_file, 'r') as f:
    og_data = yaml.load(f, Loader=yaml.SafeLoader) 

acceptance = og_data.get('dependent_variables', {})[0].get('values')

print(acceptance)
