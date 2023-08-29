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

import json

from array import array

# Number of points in gradient
nRGBs = 5

# Stop points at 0, 0.2, 0.3, 0.4, and 0.6
stops = array('d', [0.0, 0.2, 0.3, 0.4, 0.6])

# RGB values for the colors at the stops (scaled between 0 and 1)
red   = array('d', [236/255.0, 97/255.0, 33/255.0, 30/255.0, 21/255.0])
green = array('d', [228/255.0, 203/255.0, 191/255.0, 172/255.0, 121/255.0])
blue  = array('d', [241/255.0, 221/255.0, 212/255.0, 190/255.0, 133/255.0])

# Create the gradient color table
ROOT.TColor.CreateGradientColorTable(nRGBs, stops, red, green, blue, 255)
ROOT.gStyle.SetNumberContours(255)
hist =     ROOT.TH2F("hist", "hist",10, 65, 765, 8, 0, 400)
hist.SetStats(0)

Pt = []
d0 = []
eff = []

# Read the JSON file
file_path = "2.json"
with open(file_path, 'r') as f:
    json_data = json.load(f)
    
values_data = json_data.get('values', None)

for entry in values_data:
    Pt.append(float(entry['x'][0]['value']))
    d0.append(float(entry['x'][1]['value']))
    eff.append(float(entry['y'][0]['value']))

# Fill the histogram
for i in range(len(Pt)):
    # Adding 1 to ensure we start from bin 1
    x_bin = hist.GetXaxis().FindBin(Pt[i])
    y_bin = hist.GetYaxis().FindBin(d0[i])
    hist.SetBinContent(x_bin, y_bin, eff[i])

# Draw the histogram
c = ROOT.TCanvas("canvas", "Pt-do eff", 800, 600)
hist.GetXaxis().SetTitle("Pt (GeV)")
hist.GetYaxis().SetTitle("d0 (mm)")
hist.SetTitle("Muon reconstruction efficiency")
hist.Draw("COLZ")
c.Update()
c.SaveAs("code.pdf")

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

#hist= graph.GetHistogram()

def eff_func (lepton1, lepton2):

  x1= lepton1.momentum.pt()
  y1= abs(CalcD0(lepton1))
  
  x2= lepton2.momentum.pt()
  y2= abs(CalcD0(lepton2))
  
  

 
  binX1 = hist.GetXaxis().FindBin(x1)
  binY1 = hist.GetYaxis().FindBin(y1)
  
  binX2 = hist.GetXaxis().FindBin(x2)
  binY2 = hist.GetYaxis().FindBin(y2)
  
  eff_value1= hist.GetBinContent(binX1, binY1)
  eff_value2= hist.GetBinContent(binX2, binY2)
  if eff_value1 ==0:
   print(x1,y1,binX1,binY1)
  #print(eff_value1, eff_value2)
  
  rand1= random.random()
  rand2= random.random()
  global pass1
  global pass2
  pass1 = False
  pass2=False
  
  if rand1 < eff_value1:
    pass1 = True
  else:
    pass1 = False
    
  if rand2 < eff_value2:
    pass2 = True
  else:
    pass2 = False
   
  #print (rand1, eff_value1, pass1, rand2, eff_value2, pass2)
  if pass1 == True and pass2 == True:
    return True
  else:
    return False
    
  
  
hepmc_file = "tag_1_pythia8_events.hepmc"



good_event=0
with hep.open(hepmc_file) as f:
    # Loop over events in the file
    
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
      #if len(leptons) >= 2:
        
      if len(leptons) == 2:
        
        pt1 = leptons[0].momentum.pt()
        pt2 = leptons[1].momentum.pt()
        lead=leptons[0]
        sub= leptons[1]
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
          
        delta_R = particle1_vector.DeltaR(particle2_vector)
        if delta_R >= 0.2:

          cond= eff_func(lead,sub)
          if cond == True:
            good_event=good_event+1
            
      
      if len(leptons) > 2:
        
        pt1 = leptons[0].momentum.pt()
        pt2 = leptons[1].momentum.pt()
        lead=leptons[0]
        sub= leptons[1]
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
          
        delta_R = particle1_vector.DeltaR(particle2_vector)
        if delta_R >= 0.2:

          cond= eff_func(lead,sub)
          if cond== True:
            good_event=good_event+1
          if cond== False:
          
            if pass1 == False:
              leptons.remove(leptons[0])
            
            if pass2 == False:
              leptons.remove(leptons[1])
             
            if len(leptons) >= 2:
            
              for lepton in leptons:
            
                cond= eff_func(leptons[0],leptons[1])
                if cond == True:
                  good_event=good_event+1
                  break
                if  cond == False:
                  if pass1 == False:
                    leptons.remove(leptons[0])
            
                  if pass2 == False:
                    leptons.remove(leptons[1])
                if len(leptons)==1:
                  break
                  
                  
   
        
        
print("Number of passed events is: ", good_event, " event")
print("Number of expected events: ", (good_event* 0.0005221*139*1000)/20000)


              
  
