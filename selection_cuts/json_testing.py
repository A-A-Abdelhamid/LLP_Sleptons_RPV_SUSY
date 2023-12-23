import matplotlib.pyplot as plt
import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import uproot
import ROOT
from collections import Counter
import math
from ROOT import TLorentzVector
from ROOT import TEfficiency, TFile, TH1F, TGraph2DErrors, gStyle, gROOT, TColor, TLatex
from functools import reduce
from operator import mul
import json
from array import array

# CHANGE ME :)
hepmc_file = "../../run_data/run_17/Events/run_01/tag_1_pythia8_events.hepmc"

# Initialize efficiency arrays
pT = []
d0 = []
eff = []

# Read the JSON file
file_path = "Eff.json"
with open(file_path, 'r') as f:
    json_data = json.load(f)
    
values_data = json_data.get('values', None)

for entry in values_data:
    pT.append( float( entry['x'][0]['value'] ) )
    d0.append( float( entry['x'][1]['value'] ) )
    eff.append( float( entry['y'][0]['value'] ) )

print(f'pT: {pT}')
print(f"d0: {d0}")
print(f'efficiency: {eff}')

efficiency = []

for value in values_data:
    efficiency.append( [ float( value['x'][0]['value'] ), float( value['x'][1]['value'] ), float ( value['y'][0]['value'] ) ] )

print(efficiency)
