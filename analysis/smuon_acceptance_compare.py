import numpy as np
import pyhepmc as hep

og_file = "HEPData-ins1831504-v2-Smuon_acceptance.csv"
og_data = np.genfromtxt(og_file, delimiter=',')

print(og_data)
