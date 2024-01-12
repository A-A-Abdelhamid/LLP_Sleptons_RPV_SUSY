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
import json
from array import array


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
hist =     ROOT.TH2F("hist", "hist",10, 65, 765, 8, 0, 400)
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
hist.Draw("COLZ")
c.Update()
c.SaveAs("effHisto.pdf")



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
 
 
"""
"file_path = "HEPData-ins1831504-v2-pt-d0_muon_efficiency.root"
root_file = TFile.Open(file_path)
directory = root_file.GetDirectory("pt-d0 muon efficiency")
graph = directory.Get("Graph2D_y1")

hist= graph.GetHistogram()
"""

histo = ROOT.TH1F("weights","weights",200,0,1)

expected =ROOT.TH1F("Expected","Expected",1,0,1)

def eff_func (lepton):

  x= lepton.momentum.pt()
  y= abs(CalcD0(lepton))
  binX = hist.GetXaxis().FindBin(x)
  binY = hist.GetYaxis().FindBin(y)
    
  eff_value= hist.GetBinContent(binX, binY)
  return eff_value

good_event=0

def process_pairs(lepton1,lepton2):
    lead, sub = lepton1, lepton2
      
        

    particle1_vector = create_vector(lead)
    particle2_vector = create_vector(sub)
        
    delta_R = particle1_vector.DeltaR(particle2_vector)

    if delta_R >= 0.2:
      return True
        
    else:
      return False  # Exit the loop if delta_R < 0.2

def triggered(event):
    has_valid_electron = False
    has_valid_muon = False
    electron_count = 0
    lepton_eta_count = 0  # Count of leptons with eta < 2.5

    for particle in event.particles:
        if particle.status != 1:  # Consider only final state particles
          continue

        eta = CalcEta(particle)
        if abs(particle.pid) == 11:  # Electron
            if particle.momentum.pt() > 160:
                has_valid_electron = True
            elif particle.momentum.pt() > 60:
                electron_count += 1

        elif abs(particle.pid) == 13:  # Muon
            if particle.momentum.pt() > 60 and abs(eta) < 1.05:
                has_valid_muon = True

        if abs(particle.pid) in [11, 13] and abs(eta) < 2.5:
            lepton_eta_count += 1

    # Check if the event satisfies the original conditions
    if has_valid_electron or electron_count >= 2 or has_valid_muon:
        # If original conditions are met, check for the additional eta condition
        if lepton_eta_count >= 2:
            return True

    return False
    
  
hepmc_file = "tag_1_pythia8_events.hepmc"


#hist =  ROOT.TH2F("hist", "hist" ,10, 65, 765, 8, 0, 400)
count=0
weight_sum=0
nottriggered=0
with hep.open(hepmc_file) as f:
    # Loop over events in the file
    
    for event in f:
      trigger= False
      particles=[]
      leptons=[]
      signal_leptons=[]
      pt_sub=0
      pt_leading=0
      list=[]
      passtrigger=[]
      
      cond=triggered(event)
      if cond == False:
        nottriggered = nottriggered +1
        continue
        
      for particle in event.particles:
        
        
        
        if abs(particle.pid) == 13 and particle.status == 1 and particle.momentum.pt()> 65 and CalcEta(particle)> -2.5 and CalcEta(particle) < 2.5 and abs(CalcD0(particle))>3 and abs(CalcD0(particle)) <300 :
        
          leptons.append(particle)
      
      leptons.sort(key=lambda lepton: -lepton.momentum.pt())

      pt=[]
      eta=[]
      phi=[]
      mass=[]
      acc=[]
      weights= []

      if len(leptons) >= 2:
        n = len(leptons)
        for i in range(n):
          for j in range(n):
            if j > i:
              check_R = process_pairs(leptons[i],leptons[j])
              if check_R == True:
              
                if leptons[i] not in acc:
                  acc.append(leptons[i])
                  
                if leptons[j] not in acc:
                  acc.append(leptons[j])
                  
                  
        for k in range(len(acc)):
          eff= eff_func(acc[k])
          #print("pt: ", acc[k].momentum.pt()," ", CalcD0(acc[k]) , " ","eff: ", eff)
          weights.append(eff)
        #print(acc)
        #print("weights: ", weights)
          
      
        p_event= weight(weights)
        if p_event != 0:
          histo.Fill(p_event)
          
        expected.Fill(0.5,p_event)
        #print("weight: ", p_event)
        weight_sum= weight_sum + p_event
        #print("sum: ", weight_sum)
        if p_event > 0 :
          count=count+1
          #print((weight_sum))
          #histo.Fill(0,p_event)
        #print("count: ", count)
        

c = ROOT.TCanvas("canvas", "Expected", 800, 600)
expected.Draw("COLZ")
c.Update()
c.SaveAs("expected.pdf")
area = (expected.GetSumOfWeights())


print(f"Area under the histogram (number of surviving events): ", area)
bincontent =expected.GetBinContent(1)
error= expected.GetBinError(1)
print("Bin content: ",bincontent, " error = +/- ", error)
sigma=  0.0005221 * 1000 # 0.5221 fp
L = 139 #1/fb
n_gen=20000 # # of generated events
print("Expected events: ", (area*sigma*L)/n_gen, "  +/- ",((error*sigma*L)/n_gen), " events")
triggered_events= 20000- nottriggered
print ("triggered events =  ", triggered_events)
print ("ratio of triggered to total events =  ", triggered_events/20000)
print ("in paper it was= ", 66.3/93.6)

total_histogram = TH1F()
passed_histogram = TH1F()

# Fill the histograms with total events and triggered events
total_events = 20000  # Total number of events (denominator)
passed_events = triggered_events    # Number of passed events (numerator)

total_histogram.SetBinContent(1, total_events)
    

passed_histogram.SetBinContent(1, passed_events)
   

# Set uncertainties for total and passed events
etot= math.sqrt(total_events)
epass= math.sqrt(passed_events)

total_histogram.SetBinError(1, etot)
passed_histogram.SetBinError(1, epass)

eff = TEfficiency(passed_histogram, total_histogram)

print("Ratio of triggered is ", eff.GetEfficiency(1))
print("Error_Low: ",eff.GetEfficiencyErrorLow(1))
print("Error_high: ", eff.GetEfficiencyErrorUp(1))

total_histogram_p = TH1F()
passed_histogram_p = TH1F()

# Fill the histograms with total events and passed events
total_events_p = 93.6  # Total number of events (denominator)
passed_events_p = 66.3     # Number of triggered events (numerator)

total_histogram_p.SetBinContent(1, total_events_p)
    

passed_histogram_p.SetBinContent(1, passed_events_p)
   

# Set uncertainties for total and passed events
etot_p= math.sqrt(total_events_p)
epass_p= math.sqrt(passed_events_p)

total_histogram_p.SetBinError(1, etot_p)
passed_histogram_p.SetBinError(1, epass_p)

eff_p = TEfficiency(passed_histogram_p, total_histogram_p)

print("paper ratio of triggered is ", eff_p.GetEfficiency(1))
print("Error_Low: ",eff_p.GetEfficiencyErrorLow(1))
print("Error_high: ", eff_p.GetEfficiencyErrorUp(1))

#print (eff.GetEfficiency(1) - eff.GetEfficiencyErrorLow(1))
#print (eff_p.GetEfficiency(1)+eff_p.GetEfficiencyErrorUp(1))
