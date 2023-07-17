import matplotlib.pyplot as plt
import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import uproot
import ROOT
from collections import Counter

hepmc_file = "tag_1_pythia8_events.hepmc"

hist = ROOT.TH1F("pt_distribution", "Pt Distribution", 100, 0, 1000)



with hep.open(hepmc_file) as f:
    # Loop over events in the file
    for event in f:
      for particle in event.particles:
        
        if particle.status == 1 and abs(particle.pid) == 13:
           
            momentum =particle.momentum
            pt = momentum.pt()
            hist.Fill(pt)
canvas = ROOT.TCanvas("canvas", "Pt Distribution", 800, 600)
hist.Draw()

    # Customize the plot
hist.SetTitle("Final Muons Pt Distribution")
hist.GetXaxis().SetTitle("Pt (GeV)")
hist.GetYaxis().SetTitle("Number of Events")


canvas.Update()
ROOT.gROOT.GetListOfCanvases().Draw()
canvas.SaveAs("plot.pdf")
