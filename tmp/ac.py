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
from ROOT import TEfficiency, TFile, TH1F

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
  
  
hepmc_file = "tag_1_pythia8_events.hepmc"


with hep.open(hepmc_file) as f:
    # Loop over events in the file
    good_event=0
    for event in f:
      particles=[]
      leptons=[]
      signal_leptons=[]
      pt_sub=0
      pt_leading=0
      for particle in event.particles:
        
        #if particle.status == 1:
         # particles.append(particle)
          
        if abs(particle.pid) == 13 and particle.status == 1 and particle.momentum.pt()> 65 and CalcEta(particle)> -2.5 and CalcEta(particle) < 2.5 and abs(CalcD0(particle))>3 and abs(CalcD0(particle)) <300 :
        
          leptons.append(particle)
      
          
      leptons.sort(key=lambda lepton: -lepton.momentum.pt())

        # Select the top two leptons (if there are at least two)
      if len(leptons) >= 2:
        signal_leptons = leptons[:2]
        
        pt1 = signal_leptons[0].momentum.pt()
        pt2 = signal_leptons[1].momentum.pt()
        lead=signal_leptons[0]
        sub= signal_leptons[1]
        eta1 = CalcEta(lead)
        eta2 = CalcEta(sub)
        phi1= CalcPhi(lead)
        phi2=CalcPhi(sub)
        m1=lead.generated_mass
        m2=sub.generated_mass
        particle1_vector = TLorentzVector()
        particle1_vector.SetPtEtaPhiM(pt1, eta1, phi1, m1)
        particle2_vector = TLorentzVector()
        particle2_vector.SetPtEtaPhiM(pt2, eta2, phi2, m2)
 
        # Calculate "delta phi" between the two particles
        #delta_phi = particle1_vector.DeltaPhi(particle2_vector)

        
        # Calculate "delta R" between the two particles
        delta_R = particle1_vector.DeltaR(particle2_vector)
        if delta_R >= 0.2:
          good_event=good_event+1
        
        
        
      #for lepton in signal_leptons:
        #print("Selected lepton pt:", lepton.momentum.pt())
    print(good_event)
    
    # Create a ROOT histogram with a single bin
    histogram1 = TH1F()
    histogram2= TH1F()

    # Fill the histogram with your single value
    n = good_event
    d = 12135
    # Create two histograms: one for total events and one for passed events
    total_histogram = TH1F()
    passed_histogram = TH1F()

    # Fill the histograms with total events and passed events
    total_events = 20000  # Total number of trials (denominator)
    passed_events = n     # Number of successful trials (numerator)

    total_histogram.SetBinContent(1, total_events)
    

    passed_histogram.SetBinContent(1, total_events - passed_events)
   

    # Set uncertainties for total and passed events
    total_histogram.SetBinError(1, 1/math.sqrt(total_events))


    passed_histogram.SetBinError(1, 1/math.sqrt(total_events - passed_events))

    c = ROOT.TCanvas("c","c")
    # Create a TEfficiency object using the histograms
    eff = TEfficiency(passed_histogram, total_histogram)
   
    eff.SetMarkerStyle(8)
    eff.Draw('APL')
    c.SaveAs('f.pdf')


   
           
           
            

            
            
            
            
   
