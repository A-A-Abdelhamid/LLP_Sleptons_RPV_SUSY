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

histd0 = ROOT.TH1F("d0_distribution", "d0 Distribution", 100, 0, 1000) #Plot for all final muons d0

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
        pt= particle.momentum.pt()
        #All final status muons
        if particle.status == 1 and abs(particle.pid) == 13:
           
           #if pt > 65:
            histPt.Fill(pt)
           #if eta < 2.5 and eta > -2.5:
            histEta.Fill(eta)
            
            d0=CalcD0(particle)
            histd0.Fill(d0)
            
            
            
            """
            This is to get the info of muons with a range of pt
            
            if pt <=20:
            muons.append((particle.pid, particle.id, event.event_number))
            """
        # Check if the particle is a muon produced by a decaying 2000013 or -2000013
        if abs(particle.pid) == 13 and particle.production_vertex and any(p.pid in [2000013, -2000013] for p in particle.production_vertex.particles_in):
            # Get the final muon descendant of the muon
            final_muon = get_final_muon_descendant(particle)
            if final_muon is not None:
                #if final_muon.momentum.pt()> 65:
                histSignalPt.Fill(final_muon.momentum.pt())
                
                eta= CalcEta(final_muon) #Calculating final muon eta and updating the value of "eta"
                #if eta < 2.5 and eta > -2.5:
                histSgEta.Fill(eta)
                

canvasPt = ROOT.TCanvas("canvasPt", "Pt Distribution", 800, 600)
histPt.Draw()
histPt.SetTitle("Final Muons Pt Distribution")
histPt.GetXaxis().SetTitle("Pt (GeV)")
histPt.GetYaxis().SetTitle("Counts")
canvasPt.Update()
canvasPt.SaveAs("pt_plot_cut.pdf")

canvasSigPt = ROOT.TCanvas("canvasSigPt", "Signal Pt Distribution", 800, 600)
histSignalPt.Draw()
histSignalPt.SetTitle("Signal Muons Pt Distribution")
histSignalPt.GetXaxis().SetTitle("Pt (GeV)")
histSignalPt.GetYaxis().SetTitle("Counts")
canvasSigPt.Update()
canvasSigPt.SaveAs("Sig_Pt.pdf")


canvasEta = ROOT.TCanvas("canvasEta", "Eta Distribution", 800, 600)
histEta.Draw()
histEta.SetTitle("Final Muons Eta Distribution")
histEta.GetXaxis().SetTitle("Eta [unitless]")
histEta.GetYaxis().SetTitle("Counts")
canvasEta.Update()
canvasEta.SaveAs("Eta.pdf")

canvasSgEta = ROOT.TCanvas("canvasSigEta", "Signal Eta Distribution", 800, 600)
histSgEta.Draw()
histSgEta.SetTitle("Signal Muons Eta Distribution")
histSgEta.GetXaxis().SetTitle("Eta [unitless]")
histSgEta.GetYaxis().SetTitle("Counts")
canvasSgEta.Update()
canvasSgEta.SaveAs("Sig_Eta.pdf")


canvasd0 = ROOT.TCanvas("canvasd0", "d0 Distribution", 800, 600)
histd0.Draw()
histd0.SetTitle("Final Muons d0 Distribution")
histd0.GetXaxis().SetTitle("d0 [mm]")
histd0.GetYaxis().SetTitle("Counts")
canvasd0.Update()
canvasd0.SaveAs("d0.pdf")

