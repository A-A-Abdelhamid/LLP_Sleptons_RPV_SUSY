import matplotlib.pyplot as plt
import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import uproot
import ROOT
from collections import Counter
import math

hepmc_file = "tag_1_pythia8_events.hepmc"

histDeltaEta = ROOT.TH1F("dEta_distribution", "Delta Eta Distribution", 100, 0, 10)
histDeltaPhi= ROOT.TH1F("dPhi_distribution", "Delta Phi Distribution", 100, -7, 7)
histPhi= ROOT.TH1F("Phi_distribution", "Phi Distribution", 100, -4, 4)
histDeltaR= ROOT.TH1F("DeltaR_distribution", "Phi Distribution", 100, 0, 10)


deltaPhi= []
deltaR=[]
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

def CalcPhi(particle):

  momentum =particle.momentum
  px=momentum.px
  py=momentum.py
  phi = np.arctan2(py, px)
  return phi

  
with hep.open(hepmc_file) as f:
    # Loop over events in the file
    for event in f:
      muons =[]
      anti_muons=[]
      for particle in event.particles:
        
        if particle.pid== 13 and particle.status==1:
          muons.append(particle)
          phi=CalcPhi(particle)
          histPhi.Fill(phi)
        if particle.pid == -13 and particle.status==1:
          anti_muons.append(particle)
          phi=CalcPhi(particle)
          histPhi.Fill(phi)
      for m in muons:
        for am in anti_muons:
          eta1 = CalcEta(m)
          eta2 = CalcEta(am)
          delta_eta= eta1 - eta2
          phi1= CalcPhi(m)
          phi2=CalcPhi(am)
          delta_phi= phi1 - phi2
          delta_R = np.sqrt((delta_phi** 2) + (delta_eta** 2))
          histDeltaEta.Fill(delta_eta)
          histDeltaPhi.Fill(delta_phi)
          histDeltaR.Fill(delta_R)
          deltaR.append(delta_R)
          deltaPhi.append(delta_phi)
       
           
           #if pt > 65:
            #histPt.Fill(pt)
            #muons.append(particle) #get all final status muons
           #if eta < 2.5 and eta > -2.5:
            #histEta.Fill(eta)
            
            
            
            
x_line = math.pi

# Create a TLine object and set its position and properties
line = ROOT.TLine(x_line, 0, x_line, histDeltaR.GetMaximum())
line2 = ROOT.TLine(x_line, 0, x_line, histDeltaPhi.GetMaximum())
line3 = ROOT.TLine(-x_line, 0, -x_line, histDeltaPhi.GetMaximum())
line.SetLineColor(ROOT.kRed)
line2.SetLineColor(ROOT.kRed)
line3.SetLineColor(ROOT.kRed)
line.SetLineStyle(2)
line2.SetLineStyle(2)
line3.SetLineStyle(2)
"""
            
canvasDEta = ROOT.TCanvas("canvasDEta", "Delta Eta Distribution", 800, 600)
histDeltaEta.Draw()
histDeltaEta.SetTitle("Absolute Delta Eta Distribution")
histDeltaEta.GetXaxis().SetTitle("Eta [unitless]")
histDeltaEta.GetYaxis().SetTitle("Counts")
canvasDEta.Update()
canvasDEta.SaveAs("absdeltaEta.pdf")
"""
canvasdPhi = ROOT.TCanvas("canvasdPhi", "Absolute Delta Phi Distribution", 800, 600)
histDeltaPhi.Draw()
histDeltaPhi.SetTitle("Delta Phi Distribution")
histDeltaPhi.GetXaxis().SetTitle("Delta phi")
histDeltaPhi.GetYaxis().SetTitle("Counts")
line2.Draw("same")
line3.Draw("same")
canvasdPhi.Update()
canvasdPhi.SaveAs("delta_Phi_line.pdf")



canvasPhi = ROOT.TCanvas("canvasPhi", "Phi Distribution", 800, 600)
histPhi.Draw()
histPhi.SetTitle("Phi Distribution")
histPhi.GetXaxis().SetTitle("Phi")
histPhi.GetYaxis().SetTitle("Counts")
canvasPhi.Update()
canvasPhi.SaveAs("Phi.pdf")



canvasDelta = ROOT.TCanvas("canvasDelta", "Delta_R Distribution", 800, 600)
histDeltaR.Draw()
histDeltaR.SetTitle("Delta R Distribution")
histDeltaR.GetXaxis().SetTitle("Delta_R")
histDeltaR.GetYaxis().SetTitle("Counts")
line.Draw("same")
canvasDelta.Update()
canvasDelta.SaveAs("deltaR.pdf")

plt.figure(figsize=(8, 6))
plt.scatter(deltaPhi, deltaR, s=5, c='blue', label='Data points')
plt.xlabel('delta phi')
plt.ylabel('delta R')
plt.title('delt phi - delta R Plot')
#xdata=[3.14]
#ab=[500,400,300, 200, 100, 0, 100, 200, 300,400,500]
#plt.plot(ab, xdata, color='red')
plt.legend()
plt.grid(True)
plt.show()
plt.close()
plt.savefig('plot.png')
