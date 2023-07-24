import matplotlib.pyplot as plt
import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import uproot
import ROOT
from collections import Counter

hepmc_file = "tag_1_pythia8_events.hepmc"

histPt = ROOT.TH1F("pt_distribution", "Pt Distribution", 100, 0, 1000) #Plot for all final muons pts
histSignalPt= ROOT.TH1F("signalpt_distribution", "Signal Pt Distribution", 100, 0, 1000) #Plot for signal muons pts

histEta = ROOT.TH1F("eta_distribution", "Eta Distribution", 100, -3, 3) #Plot for all final muons eta

histSgEta = ROOT.TH1F("signaleta_distribution", "Eta Distribution", 100, -3, 3) #Plot for signal muons eta

histd0 = ROOT.TH1F("d0_distribution", "d0 Distribution", 100, 0, 1) #Plot for all final muons d0


dataDo=[]

def get_final_muon_descendant(particle):
    """
    Get the final state muon descendant of a given particle.

    """
    # Check if the particle itself is a final state muon
    if particle.status == 1 and abs(particle.pid) == 13:
        return particle
    # If the particle has an end vertex, check its descendants recursively
    elif particle.end_vertex:
        for p in particle.end_vertex.particles_out:
            final_muon = get_final_muon_descendant(p)
            if final_muon is not None:
                return final_muon
    # If the particle is not a final state muon and does not have an end vertex, return None
    return None

muons = []

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
          
with hep.open(hepmc_file) as f:
    # Loop over events in the file
    for event in f:
      for particle in event.particles:
        eta = CalcEta(particle)
        
        
        
           
           #if pt > 65:
            #histPt.Fill(pt)
            #muons.append(particle) #get all final status muons
           #if eta < 2.5 and eta > -2.5:
            #histEta.Fill(eta)
            
            
            
            
            
        """
            This is to get the info of muons with a range of pt
            
            if pt <=20:
            muons.append((particle.pid, particle.id, event.event_number))
        """
        # Check if the particle is a muon produced by a decaying 2000013 or -2000013
        if abs(particle.pid) == 13 and particle.production_vertex and any(p.pid in [2000013, -2000013] for p in particle.production_vertex.particles_in):
            d0=CalcD0(particle)
            histd0.Fill(d0)
            dataDo.append(d0)
            # Get the final muon descendant of the muon
        
            final_muon = get_final_muon_descendant(particle)
            if final_muon is not None:
                muons.append(final_muon)
                if final_muon.momentum.pt()> 65:
                  histSignalPt.Fill(final_muon.momentum.pt())
                
                
                eta= CalcEta(final_muon) #Calculating final muon eta and updating the value of "eta"
                if eta < 2.5 and eta > -2.5:
                  histSgEta.Fill(eta)
                  #d0=CalcD0(final_muon)
                  #histd0.Fill(d0)
        
        if abs(particle.pid) == 13 and particle.status == 1 and particle not in muons:
          # This is a final state muon that did not come from a 2000013 or -2000013 vertex
           # Proceed with your analysis...

           pt= particle.momentum.pt()
           if pt> 65:
             histPt.Fill(pt)
           
           eta= CalcEta (particle)
           if eta < 2.5 and eta > -2.5:
             histEta.Fill(eta)
             
             
            
canvasPt = ROOT.TCanvas("canvasPt", "Pt Distribution", 800, 600)
histPt.Draw()
histPt.SetTitle("Non-Signal Muons Pt > 65 GeV Distribution")
histPt.GetXaxis().SetTitle("Pt (GeV)")
histPt.GetYaxis().SetTitle("Counts")
canvasPt.Update()
canvasPt.SaveAs("pt_NonSignal_Cut.pdf")

canvasSigPt = ROOT.TCanvas("canvasSigPt", "Signal Pt Distribution", 800, 600)
histSignalPt.Draw()
histSignalPt.SetTitle("Signal Muons Pt > 65 GeV Distribution")
histSignalPt.GetXaxis().SetTitle("Pt (GeV)")
histSignalPt.GetYaxis().SetTitle("Counts")
canvasSigPt.Update()
canvasSigPt.SaveAs("Sig_Pt_Cut.pdf")


canvasEta = ROOT.TCanvas("canvasEta", "Eta Distribution", 800, 600)
histEta.Draw()
histEta.SetTitle("Non Signal Muons |Eta| > 2.5  Distribution")
histEta.GetXaxis().SetTitle("Eta [unitless]")
histEta.GetYaxis().SetTitle("Counts")
canvasEta.Update()
canvasEta.SaveAs("EtaNonSignal_Cut.pdf")

canvasSgEta = ROOT.TCanvas("canvasSigEta", "Signal Eta Distribution", 800, 600)
histSgEta.Draw()
histSgEta.SetTitle("Signal Muons |Eta| > 2.5 Distribution")
histSgEta.GetXaxis().SetTitle("Eta [unitless]")
histSgEta.GetYaxis().SetTitle("Counts")
canvasSgEta.Update()
canvasSgEta.SaveAs("Sig_Eta_Cut.pdf")


canvasd0 = ROOT.TCanvas("canvasd0", "d0 Distribution", 800, 600)
histd0.Draw()
histd0.SetTitle("Signal muons d0 Distribution")
histd0.GetXaxis().SetTitle("d0 [mm]")
histd0.GetYaxis().SetTitle("Counts")
canvasd0.Update()
canvasd0.SaveAs("d0.pdf")

data_d0 = np.array([histd0.GetBinContent(i) for i in range(1, histd0.GetNbinsX() + 1)])
def calculate_mode(data):
    counts = Counter(data)
    mode = max(counts, key=counts.get)
    return mode

def calculate_median(data):
    median = np.median(data)
    return median

def calculate_mean(data):
    mean = np.mean(data)
    return mean
"""    
mode_d0 = calculate_mode(data_d0)
median_d0 = calculate_median(data_d0)
mean_d0 = calculate_mean(data_d0)

print("d0 Distribution:")
print("Mode:", mode_d0)
print("Median:", median_d0)
print("Mean:", mean_d0)


rounded_d0 = np.round(data_d0, decimals=2)
d0_counter = Counter(rounded_d0)
print("Frequency of each d0 value (rounded to two decimal places):")
for d0_value, frequency in d0_counter.items():
    print(f"{d0_value:.2f}: {frequency} counts")

"""
