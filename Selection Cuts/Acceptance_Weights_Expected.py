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
hepmc_file = "../../run_data/run_15/Events/run_01/tag_1_pythia8_events.hepmc"

# Number of points in gradient of the Eff histogram
nRGBs = 5

# Stop points at 0, 0.2, 0.3, 0.4, and 0.6
stops = array('d', [0.0, 0.2, 0.3, 0.4, 0.6])  # 'd' denotes double

# RGB values for the colors at the stops (scaled between 0 and 1)
red   = array('d', [236/255.0, 97/255.0, 33/255.0, 30/255.0, 21/255.0])
green = array('d', [228/255.0, 203/255.0, 191/255.0, 172/255.0, 121/255.0])
blue  = array('d', [241/255.0, 221/255.0, 212/255.0, 190/255.0, 133/255.0])

# Create the gradient color table
ROOT.TColor.CreateGradientColorTable(nRGBs, stops, red, green, blue, 255)
ROOT.gStyle.SetNumberContours(255)
hist = ROOT.TH2F("hist", "hist",10, 65, 765, 8, 0, 400)
hist.SetStats(0)
# Initialize the ROOT TArrays
Pt = []
d0 = []
eff = []

# Read the JSON file
file_path = "Eff.json"
with open(file_path, 'r') as f:
    json_data = json.load(f)
    
values_data = json_data.get('values', None)

for entry in values_data:
    Pt.append( float( entry['x'][0]['value'] ) )
    d0.append( float( entry['x'][1]['value'] ) )
    eff.append( float( entry['y'][0]['value'] ) )

# Fill the histogram
for i in range( len(Pt) ):
    # Adding 1 to ensure we start from bin 1 ### TODO Is something missing here?
    x_bin = hist.GetXaxis().FindBin( Pt[i] )
    y_bin = hist.GetYaxis().FindBin( d0[i] )
    hist.SetBinContent( x_bin, y_bin, eff[i] )

# Draw the histogram
cH = ROOT.TCanvas("canvasH", "Pt-do eff", 800, 600)
hist.GetXaxis().SetTitle("Pt (GeV)")
hist.GetYaxis().SetTitle("d0 (mm)")
hist.SetTitle("Muon reconstruction efficiency")
hist.Draw("COLZ")
cH.Update()
cH.SaveAs("effHisto.pdf")

# pT conversion from MeV to GeV
def mev_to_gev(mev):
    return mev * 10**-3

def create_vector(particle):
    vector = TLorentzVector()
    pt = mev_to_gev( particle.momentum.pt() )
    eta = CalcEta(particle)
    phi = CalcPhi(particle)
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
    
    # Combine both terms and subtract from 1
    result = 1 - (first_term + second_term)
    
    return result

def CalcEta(particle):
  momentum = particle.momentum
  pt = mev_to_gev( momentum.pt() )
  px = momentum.px
  py = momentum.py
  pz = momentum.pz
  p = momentum.length()
  if pz == p:
    etaC = np.inf  # or a large number
  elif pz == -p:
    etaC = -np.inf  # or a large negative number
  else:
    etaC = np.arctanh(pz / p)
  return etaC
  
def CalcD0(particle):
  """
  Calculates d0 of a particle's track
  Assuming lieanr tracks since there is no mgentic field
  d0 = production vertex vector X produced particle momentum vector
  d0 is in the transverse plane
  d0 = [vertex x spatial component * (Py/Pt)] - [vertex y spatial component * (Px/Pt)]
  """
  momentum = particle.momentum
  pt = momentum.pt()
  px = momentum.px
  py = momentum.py
  
  ver = particle.production_vertex.position
  xver = ver.x
  yver = ver.y

  d0 = (xver* (py/pt)) - (yver* (px/pt))
  return d0

def CalcPhi(particle):
  momentum = particle.momentum
  px = momentum.px
  py = momentum.py
  phi = np.arctan2(py, px)
  return phi

expected = ROOT.TH1F("Expected","Expected Number of Events",1,0,1)

def eff_func(lepton):
  x = mev_to_gev( lepton.momentum.pt() )
  y = abs( CalcD0(lepton) )
  binX = hist.GetXaxis().FindBin(x)
  binY = hist.GetYaxis().FindBin(y)
    
  eff_value = hist.GetBinContent(binX, binY)
  return eff_value

def process_pairs(lepton1,lepton2):
    particle1_vector = create_vector(lepton1)
    particle2_vector = create_vector(lepton2)
        
    delta_R = particle1_vector.DeltaR(particle2_vector)

    if delta_R  >= 0.2:
      return True
    else:
      return False 

# TODO Get rid of overloaded f variable (see .json file open() @43)
with hep.open(hepmc_file) as f:
    for event in f:
        leptons = []
        for particle in event.particles:
            # TODO @170 can be condensed with a boolean function.
            if abs(particle.pid) == 13 and particle.status == 1 and mev_to_gev( particle.momentum.pt() ) > 65 and CalcEta(particle) > -2.5 and CalcEta(particle) < 2.5 and abs( CalcD0(particle) ) > 3 and abs( CalcD0(particle) ) < 300 :
                leptons.append(particle)
        leptons.sort( key=lambda lepton: -lepton.momentum.pt() )
        acc = [] #Accepted leptons
        weights = []
        if len(leptons) >= 2:
            n = len(leptons)
            for i in range(n):
                for j in range(n):
                    if j > i:
                        check_R = process_pairs( leptons[i],leptons[j] )
                        if check_R == True:
                            if leptons[i] not in acc:
                                acc.append( leptons[i] )
                            if leptons[j] not in acc:
                                acc.append( leptons[j] )
            for k in range( len(acc) ):
                eff = eff_func( acc[k] )
                weights.append(eff)
            p_event = weight(weights)
            expected.Fill(0.5, p_event)

c = ROOT.TCanvas("canvas", "Expected", 800, 600)
expected.Draw("COLZ")
c.Update()
c.SaveAs("expected.pdf")
area = ( expected.GetSumOfWeights() )

print(f"Area under the histogram (number of surviving events): ", area)
bincontent = expected.GetBinContent(1)
error = expected.GetBinError(1)
print("Bin content: ", bincontent, " error = +/- ", error)
sigma =  0.0005221 * 1000 # 0.5221 fp
L = 139 #1/fb
n_gen = 20000 # # of generated events
print("Expected events: ", (area * sigma * L) / n_gen, "  +/- ",( (error * sigma * L) / n_gen), " events")
