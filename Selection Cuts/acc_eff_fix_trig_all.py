import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import ROOT
import math
from ROOT import TLorentzVector
from ROOT import Math
from ROOT import TEfficiency, TFile, TH1F, TGraph2DErrors, gStyle, gROOT, TColor, TLatex
from functools import reduce
from operator import mul
import json
from array import array

hepmc_file_10ns = "/Users/alaa/Downloads/MG5_aMC_v3_5_4/10ns_600GeV/Events/run_01/tag_1_pythia8_events.hepmc"

hepmc_file_1ns = "/Users/alaa/Downloads/MG5_aMC_v3_5_4/1ns_600GeV/Events/run_01/tag_1_pythia8_events.hepmc"

hepmc_file_zero_dot_1ns = "/Users/alaa/Downloads/MG5_aMC_v3_5_4/0.1ns_600GeV/Events/run_01/tag_1_pythia8_events.hepmc"


hepmc_file_zero_zero_1ns = "/Users/alaa/Downloads/MG5_aMC_v3_5_4/0.01ns_600GeV/Events/run_01/tag_1_pythia8_events.hepmc"




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
hist_eff =     ROOT.TH2F("hist", "hist",10, 65, 765, 8, 0, 400)
hist_eff.SetStats(0)

Pt = []
d0 = []
eff = []

# Read the JSON file
file_path = "Eff.json"
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
    x_bin = hist_eff.GetXaxis().FindBin(Pt[i])
    y_bin = hist_eff.GetYaxis().FindBin(d0[i])
    hist_eff.SetBinContent(x_bin, y_bin, eff[i])

# Draw the histogram
c = ROOT.TCanvas("canvas", "Pt-do eff", 800, 600)
hist_eff.Draw("COLZ")
c.Update()
c.SaveAs("effHisto.pdf")


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
  px=momentum.px
  py=momentum.py
  pz=momentum.pz
  E=momentum.e
  vector = ROOT.Math.PxPyPzEVector(px, py, pz, E)
 
  eta= vector.Eta()
  return eta
  
def CalcPhi(particle):
  momentum = particle.momentum
  px=momentum.px
  py=momentum.py
  pz=momentum.pz
  E=momentum.e
  vector = ROOT.Math.PxPyPzEVector(px, py, pz, E)

  phi= vector.Phi()
  return phi
  

def CalcD0(particle):
    ver = particle.production_vertex.position
    vx = ver.x
    vy = ver.y
    #vz = ver.z

    momentum = particle.momentum
    px = momentum.px
    py = momentum.py
    #pz = momentum.pz

    # Calculate transverse position vector
    v0_xy = ROOT.TVector3(vx, vy, 0)
    v0_xy_Mag = (vx**2 + vy**2)**0.5
    # Calculate transverse momentum vector
    p_xy = ROOT.TVector3(px, py, 0)

    # Calculate delta phi directly
    d_phi = ROOT.TVector2.Phi_mpi_pi(p_xy.DeltaPhi(v0_xy))

    # Calculate transfer impact parameter using L_xy * sin(phi)
    transfer_impact_parameter = v0_xy_Mag * ROOT.TMath.Sin(d_phi)

    return transfer_impact_parameter


def CreateVec(particle):
  momentum = particle.momentum
  pt = momentum.pt()
  eta= CalcEta(particle)
  phi= CalcPhi(particle)
  vec= ROOT.TVector3()
  vec.SetPtEtaPhi(pt,eta,phi)
  return vec
  
def eff_func (lepton):

  x= lepton.momentum.pt()
  y= abs(CalcD0(lepton))
  binX = hist_eff.GetXaxis().FindBin(x)
  binY = hist_eff.GetYaxis().FindBin(y)
    
  eff_value= hist_eff.GetBinContent(binX, binY)
  return eff_value

    
hist_10ns = ROOT.TH1F("Yield_10ns_600GeV","Yield_10ns",1,0,1)
hist_1ns = ROOT.TH1F("Yield_1ns_600GeV","Yield_1ns",1,0,1)
hist_zero_zero_1ns = ROOT.TH1F("Yield_0.01ns_600GeV","Yield_0.01ns",1,0,1)
hist = ROOT.TH1F("Yield_600GeV","Yield",1,0,1)

with hep.open(hepmc_file_10ns) as f:
  count_10ns=0
  
  for event in f:
    
    trigger= False
    
    has_valid_electron = False
    has_valid_muon = False
    electron_count = 0
   
    leptons_10ns=[]
    for particle in event.particles:
    
      if abs(particle.pid) == 13 or abs(particle.pid)==11:
      
        if particle.status == 1:
          leptons_10ns.append(particle)
          eta= CalcEta(particle)
          
          if abs(particle.pid)==11 and particle.momentum.pt() > 60:
            electron_count += 1
            if particle.momentum.pt() > 160:
              has_valid_electron = True
          
          if abs(particle.pid) == 13 and particle.momentum.pt() > 60 and abs(eta) < 1.07:
            
            has_valid_muon = True
            
    if (has_valid_electron or electron_count >= 2 or has_valid_muon):
      trigger= True
      
    if trigger == False:
      continue
      
    leptons_10ns = sorted(leptons_10ns, key=lambda p: p.momentum.pt(), reverse=True)
    if abs(leptons_10ns[0].pid) == 13 and abs(leptons_10ns[1].pid) == 13:
      if abs(CalcEta(leptons_10ns[0])) >= 2.5 or abs(CalcEta(leptons_10ns[1])) >= 2.5:
        continue
      if leptons_10ns[0].momentum.pt() < 65 or leptons_10ns[1].momentum.pt() < 65:
        continue
        
      if abs(CalcD0(leptons_10ns[0])) <3 or abs(CalcD0(leptons_10ns[1])) < 3:
        continue
        
      # Leave this for the 10ns
      if abs(CalcEta(leptons_10ns[0])) > 1.07 or abs(CalcEta(leptons_10ns[1])) > 1.07:
        continue
      
    
      vec0= CreateVec(leptons_10ns[0])
      vec1= CreateVec(leptons_10ns[1])
      
      if abs(vec0.DeltaR(vec1)) < 0.2:
        continue

      count_10ns=count_10ns+1
      eff1= eff_func(leptons_10ns[0])
      eff2= eff_func(leptons_10ns[1])
      eff=[eff1,eff2]
      p_event= weight(eff)
      hist_10ns.Fill(0.5, p_event)
      
      
      
print("Acceptance for 600GeV 10 ns is ", count_10ns, " out of 20000", " = ", count_10ns/20000)


with hep.open(hepmc_file_1ns) as f:
  count_1ns=0
  
  for event in f:
    
    trigger= False
    
    has_valid_electron = False
    has_valid_muon = False
    electron_count = 0
   
    leptons_1ns=[]
    for particle in event.particles:
    
      if abs(particle.pid) == 13 or abs(particle.pid)==11:
      
        if particle.status == 1:
          leptons_1ns.append(particle)
          eta= CalcEta(particle)
          
          if abs(particle.pid)==11 and particle.momentum.pt() > 60:
            electron_count += 1
            if particle.momentum.pt() > 160:
              has_valid_electron = True
          
          if abs(particle.pid) == 13 and particle.momentum.pt() > 60 and abs(eta) < 1.07:
            
            has_valid_muon = True
            
    if (has_valid_electron or electron_count >= 2 or has_valid_muon):
      trigger= True
      
    if trigger == False:
      continue
      
    leptons_1ns = sorted(leptons_10ns, key=lambda p: p.momentum.pt(), reverse=True)
    if abs(leptons_1ns[0].pid) == 13 and abs(leptons_1ns[1].pid) == 13:
      if abs(CalcEta(leptons_1ns[0])) >= 2.5 or abs(CalcEta(leptons_1ns[1])) >= 2.5:
        continue
      if leptons_1ns[0].momentum.pt() < 65 or leptons_1ns[1].momentum.pt() < 65:
        continue
        
      if abs(CalcD0(leptons_1ns[0])) <3 or abs(CalcD0(leptons_1ns[1])) < 3:
        continue
        
      # Leave this for the 10ns
      #if abs(CalcEta(leptons_10ns[0])) > 1.07 or abs(CalcEta(leptons_10ns[1])) > 1.07:
      #  continue
      
    
      vec0= CreateVec(leptons_1ns[0])
      vec1= CreateVec(leptons_1ns[1])
      
      if abs(vec0.DeltaR(vec1)) < 0.2:
        continue

      count_1ns=count_1ns+1
      eff1= eff_func(leptons_1ns[0])
      eff2= eff_func(leptons_1ns[1])
      eff=[eff1,eff2]
      p_event= weight(eff)
      hist_1ns.Fill(0.5, p_event)
      
      
      
print("Acceptance for 600GeV 1 ns is ", count_1ns, " out of 20000", " = ", count_1ns/20000)



with hep.open(hepmc_file_zero_dot_1ns) as f:
  count=0
  
  for event in f:
    trigger= False
    
    has_valid_electron = False
    has_valid_muon = False
    electron_count = 0
    
    leptons=[]
    for particle in event.particles:
    
      if abs(particle.pid) == 13 or abs(particle.pid)==11:
      
        if particle.status == 1:
          leptons.append(particle)
          eta= CalcEta(particle)
          
          if abs(particle.pid)==11 and particle.momentum.pt() > 60:
            electron_count += 1
            if particle.momentum.pt() > 160:
              has_valid_electron = True
          
          if abs(particle.pid) == 13 and particle.momentum.pt() > 60 and abs(eta) < 1.07:  # Muon
            
            has_valid_muon = True
        
    if (has_valid_electron or electron_count >= 2 or has_valid_muon):
      trigger= True
      
    if trigger == False:
      continue
        
    leptons = sorted(leptons, key=lambda p: p.momentum.pt(), reverse=True)
    if abs(leptons[0].pid) == 13 and abs(leptons[1].pid) == 13:
      if abs(CalcEta(leptons[0])) >= 2.5 or abs(CalcEta(leptons[1])) >= 2.5:
        continue
      if leptons[0].momentum.pt() < 65 or leptons[1].momentum.pt() < 65:
        continue
        
      if abs(CalcD0(leptons[0])) <3 or abs(CalcD0(leptons[1])) < 3:
        continue
        
      #if abs(CalcEta(leptons[0])) > 1.07 or abs(CalcEta(leptons[1])) > 1.07:
        #continue
      
    
      vec0= CreateVec(leptons[0])
      vec1= CreateVec(leptons[1])
      
      if abs(vec0.DeltaR(vec1)) < 0.2:
        continue

      count=count+1
      
      eff1= eff_func(leptons[0])
      eff2= eff_func(leptons[1])
      eff=[eff1,eff2]
      p_event= weight(eff)
      hist.Fill(0.5, p_event)
      
      
print("Acceptance for 600GeV 0.1 ns is ", count, " out of 20000", " = ", count/20000)

      
with hep.open(hepmc_file_zero_zero_1ns) as f:
  count_zero_zero_1ns=0
  
  for event in f:
    trigger= False
    
    has_valid_electron = False
    has_valid_muon = False
    electron_count = 0
    
    leptons_zero_zero_1ns=[]
    for particle in event.particles:
    
      if abs(particle.pid) == 13 or abs(particle.pid)==11:
      
        if particle.status == 1:
          leptons_zero_zero_1ns.append(particle)
          eta= CalcEta(particle)
          
          if abs(particle.pid)==11 and particle.momentum.pt() > 60:
            electron_count += 1
            if particle.momentum.pt() > 160:
              has_valid_electron = True
          
          if abs(particle.pid) == 13 and particle.momentum.pt() > 60 and abs(eta) < 1.07:  # Muon
            
            has_valid_muon = True
        
    if (has_valid_electron or electron_count >= 2 or has_valid_muon):
      trigger= True
      
    if trigger == False:
      continue
        
    leptons_zero_zero_1ns = sorted(leptons_zero_zero_1ns, key=lambda p: p.momentum.pt(), reverse=True)
    if abs(leptons_zero_zero_1ns[0].pid) == 13 and abs(leptons_zero_zero_1ns[1].pid) == 13:
      if abs(CalcEta(leptons_zero_zero_1ns[0])) >= 2.5 or abs(CalcEta(leptons_zero_zero_1ns[1])) >= 2.5:
        continue
      if leptons_zero_zero_1ns[0].momentum.pt() < 65 or leptons_zero_zero_1ns[1].momentum.pt() < 65:
        continue
        
      if abs(CalcD0(leptons_zero_zero_1ns[0])) <3 or abs(CalcD0(leptons_zero_zero_1ns[1])) < 3:
        continue
        
      #if abs(CalcEta(leptons[0])) > 1.07 or abs(CalcEta(leptons[1])) > 1.07:
        #continue
      
    
      vec0= CreateVec(leptons_zero_zero_1ns[0])
      vec1= CreateVec(leptons_zero_zero_1ns[1])
      
      if abs(vec0.DeltaR(vec1)) < 0.2:
        continue

      count_zero_zero_1ns=count_zero_zero_1ns+1
      
      eff1= eff_func(leptons_zero_zero_1ns[0])
      eff2= eff_func(leptons_zero_zero_1ns[1])
      eff=[eff1,eff2]
      p_event= weight(eff)
      hist_zero_zero_1ns.Fill(0.5, p_event)
      
      
print("Acceptance for 600GeV 0.01 ns is ", count_zero_zero_1ns, " out of 20000", " = ", count_zero_zero_1ns/20000)


c_10ns = ROOT.TCanvas("canvas_10", "Yield 10ns", 800, 600)
hist_10ns.Draw()
c_10ns.Update()
c_10ns.SaveAs("Yield_10ns_600GeV.pdf")

c_1ns = ROOT.TCanvas("canvas_1ns", "Yield 1ns", 800, 600)
hist_1ns.Draw()
c_1ns.Update()
c_1ns.SaveAs("Yield_1ns_600GeV.pdf")


c = ROOT.TCanvas("canvas", "Yield 0.1", 800, 600)
hist.Draw()
c.Update()
c.SaveAs("Yield_0.1ns_600GeV.pdf")

c_0_0_1ns = ROOT.TCanvas("canvas", "Yield_0.01ns", 800, 600)
hist_zero_zero_1ns.Draw()
c_0_0_1ns.Update()
c_0_0_1ns.SaveAs("Yield_0.01ns_600GeV.pdf")
