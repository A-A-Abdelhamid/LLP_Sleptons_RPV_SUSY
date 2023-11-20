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
import random
from functools import reduce
from operator import mul

def create_vector(particle):
    vector = TLorentzVector()
    pt = particle.momentum.pt()
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
  """
  Calculate eta of a particle
  """
  momentum =particle.momentum
  pt = momentum.pt()
  px=momentum.px
  py=momentum.py
  pz=momentum.pz
  p=momentum.length()
  if pz == p:
    etaC = np.inf  # or a large number
  elif pz == -p:
    etaC = -np.inf  # or a large negative number
  else:
    etaC = np.arctanh(pz/p)
  return etaC
  

def CalcD0(particle):

  """
  Calculates d0 of a particle's track
  Assuming lieanr tracks since there is no mgentic field
  d0 = production vertex vector X produced particle momentum vector
  d0 is in the transverse plane
  d0 = [vertex x spatial component * (Py/Pt)] - [vertex y spatial component * (Px/Pt)]
  """
  momentum =particle.momentum
  pt = momentum.pt()
  px=momentum.px
  py=momentum.py
  
  ver= particle.production_vertex.position
  xver= ver.x
  yver= ver.y

  d0= (xver* (py/pt)) - (yver* (px/pt))
  return d0

def CalcPhi(particle):

  momentum =particle.momentum
  px=momentum.px
  py=momentum.py
  phi = np.arctan2(py, px)
  return phi
 
 
file_path = "HEPData-ins1831504-v2-pt-d0_muon_efficiency.root"
root_file = TFile.Open(file_path)
directory = root_file.GetDirectory("pt-d0 muon efficiency")
graph = directory.Get("Graph2D_y1")

hist= graph.GetHistogram()
histo = ROOT.TH1F("hist", "Acceptance x Efficiency", 1, 0, 1)
def eff_func (lepton):

  x= lepton.momentum.pt()
  y= abs(CalcD0(lepton))
  binX = hist.GetXaxis().FindBin(x)
  binY = hist.GetYaxis().FindBin(y)
    
  eff_value= hist.GetBinContent(binX, binY)
  return eff_value

good_event=0

def process_pairs(leptons):
    acc=[]
    while len(leptons) >= 2:
      
        lead, sub = leptons[0], leptons[1]

        particle1_vector = create_vector(lead)
        particle2_vector = create_vector(sub)
        
        delta_R = particle1_vector.DeltaR(particle2_vector)

        if delta_R >= 0.2:
          leptons.append(leptons[0])
          leptons
          
          break
        
        else:
            break  # Exit the loop if delta_R < 0.2

    return good_event
  
hepmc_file = "tag_1_pythia8_events.hepmc"


#hist =  ROOT.TH2F("hist", "hist" ,10, 65, 765, 8, 0, 400)

with hep.open(hepmc_file) as f:
    # Loop over events in the file
    
    for event in f:
      particles=[]
      leptons=[]
      signal_leptons=[]
      pt_sub=0
      pt_leading=0
      list=[]
      for particle in event.particles:
        
        #if particle.status == 1:
         # particles.append(particle)
          
        if abs(particle.pid) == 13 and particle.status == 1 and particle.momentum.pt()> 65 and CalcEta(particle)> -2.5 and CalcEta(particle) < 2.5 and abs(CalcD0(particle))>3 and abs(CalcD0(particle)) <300 :
        
          leptons.append(particle)
      
          
      leptons.sort(key=lambda lepton: -lepton.momentum.pt())

        # Select the top two leptons (if there are at least two)
      #if len(leptons) >= 2:
      
      pt=[]
      eta=[]
      phi=[]
      mass=[]
      if len(leptons) >= 2:
      
        n = len(leptons)
        for i in range(n):
          if len(pt) <= i:
            pt.append([])  # Create a new list at pt[i] if it does not exist
            pt[i].append(leptons[i].momentum.pt())
          if len(eta) <= i:
            eta.append([])  # Create a new list at pt[i] if it does not exist
            eta[i].append(CalcEta(leptons[i]))
            
          if len(phi) <= i:
            phi.append([])  # Create a new list at pt[i] if it does not exist
            phi[i].append(CalcPhi(leptons[i]))
            
          if len(mass) <= i:
            mass.append([])  # Create a new list at pt[i] if it does not exist
            mass[i].append(leptons[i].generated_mass)
