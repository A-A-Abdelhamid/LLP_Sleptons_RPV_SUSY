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

# Read the JSON file
file_path = "Eff.json"
with open(file_path, 'r') as f:
    json_data = json.load(f)
    
values_data = json_data.get('values', None)

pT_array = []
d0_array = []
efficiency_array = []

for value in values_data:
    pT_array.append( float( value['x'][0]['value'] ) )
    d0_array.append( float( value['x'][1]['value'] ) )
    efficiency_array.append( [ float( value['x'][0]['value'] ), float( value['x'][1]['value'] ), float( value['y'][0]['value'] ) ] )

# pT conversion from MeV to GeV
def mev_to_gev(mev):
    return mev * 10**-3

# Why not use particle.momentum.eta()?
def calc_eta(particle):
    pt = mev_to_gev( particle.momentum.pt() )
    px = particle.momentum.px
    py = particle.momentum.py
    pz = particle.momentum.pz
    p = particle.momentum.length()
    # TODO Pretty sure the following lines are unnecessary. Will confirm later.
    if pz == p:
        etaC = np.inf  # or a large number
    elif pz == -p:
      etaC = -np.inf  # or a large negative number
    else:
        etaC = np.arctanh(pz / p)
    return etaC

def calc_phi(particle):
    px = particle.momentum.px
    py = particle.momentum.py
    return np.arctan2(py, px)

def create_vector(particle):
    vector = TLorentzVector()
    pt = mev_to_gev( particle.momentum.pt() )
    eta = calc_eta(particle)
    phi = calc_phi(particle)
    mass = particle.generated_mass
    vector.SetPtEtaPhiM(pt, eta, phi, mass)
    return vector

def weight(e_list):
    # Calculate the first term: Product of (1 - e_i) for i=1 to n
    first_term = reduce(mul, [(1 - e) for e in e_list], 1)
    
    # Calculate the second term: Summation for i=1 to n of (e_i * Product of (1 - e_j) for j!=i)
    second_term = 0
    n = len(e_list)
    for i in range(n):
        e_i = e_list[i]
        remaining_elements = e_list[:i] + e_list[i+1:]
        prod_remaining = reduce(mul, [(1 - e) for e in remaining_elements], 1)
        second_term += e_i * prod_remaining
    
    return 1 - (first_term + second_term)
  
def calc_d0(particle):
    """
    Assuming linear tracks since there is no magnetic field
    d0 = production vertex vector X produced particle momentum vector
    d0 = [vertex x spatial component * (Py/Pt)] - [vertex y spatial component * (Px/Pt)]
    """
    pt = particle.momentum.pt()
    px = particle.momentum.px
    py = particle.momentum.py
  
    ver = particle.production_vertex.position
    xver = ver.x
    yver = ver.y
    
    return (xver* (py/pt)) - (yver* (px/pt))


# Return the bin in which a value would be found
# NOTE This functions properly when all bins are the same size
def bin_finder(value, bin_array):
    bin_width = bin_array[1] - bin_array[0]
    containing_bin = bin_array[0]
    num_bins = len(bin_array)
    for b in bin_array:
        if value <= b + (bin_width / 2):
            containing_bin = b
            break
        if b == bin_array[num_bins - 1]:
            if value > b + (bin_width / 2):
                return 0
    return containing_bin

def get_efficiency(particle):
    pt = mev_to_gev( particle.momentum.pt() )
    d0 = abs( calc_d0(particle) )

    pT_bin = bin_finder( pt, np.unique(pT_array) )
    d0_bin = bin_finder( d0, np.unique(d0_array) )

    eff_value = 0
    for momentum, impact, efficiency in efficiency_array:
        if (momentum, impact) == (pT_bin, d0_bin):
            eff_value = efficiency
            break

    return eff_value

def delta_r_cut(particle1, particle2):
    particle1_vector = create_vector(particle1)
    particle2_vector = create_vector(particle2)
        
    delta_r = particle1_vector.DeltaR(particle2_vector)

    if delta_r  >= 0.2:
      return True
    else:
      return False 

# TODO All constants should be variables.
def passes_first_cuts(particle):
    if abs(particle.pid) == 13 and particle.status == 1:
        if  mev_to_gev( particle.momentum.pt() ) > 65:
            if calc_eta(particle) > -2.5 and calc_eta(particle) < 2.5:
                if abs( calc_d0(particle) ) > 3 and abs( calc_d0(particle) ) < 300 :
                    return True
    return False

results = []

with hep.open(hepmc_file) as hf:
    for event in hf:
        leptons = []
        for particle in event.particles:
            if passes_first_cuts(particle):
                leptons.append(particle)
        leptons.sort( key=lambda particle: -particle.momentum.pt() )
        acc = [] #Accepted leptons
        weights = []
        if len(leptons) >= 2:
            n = len(leptons)
            for i in range(n):
                for j in range(n):
                    if j > i:
                        check_r = delta_r_cut( leptons[i],leptons[j] )
                        if check_r == True:
                            if leptons[i] not in acc:
                                acc.append( leptons[i] )
                            if leptons[j] not in acc:
                                acc.append( leptons[j] )
            for k in range( len(acc) ):
                eff = get_efficiency( acc[k] )
                weights.append(eff)
            p_event = weight(weights)
            results.append(p_event)

print(results)
np.save('cut_data.npy', results)
