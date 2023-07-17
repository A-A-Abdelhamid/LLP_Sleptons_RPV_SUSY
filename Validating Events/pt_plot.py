import matplotlib.pyplot as plt
import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import uproot
import ROOT
from collections import Counter

def plot_pt_distribution(hepmc_file):
    # Create a histogram to store the pT distribution
    hist = ROOT.TH1F("pt_distribution", "Pt Distribution", 100, 0, 500)
    
    # Open the HepMC file
    with hep.open(hepmc_file) as f:
        # Loop over events in the file
        for event in f:
            # Check if there is a muon and an antimuon in the event
            pids = [particle.pid for particle in event.particles]
            if 13 in pids and -13 in pids:
                # Loop over particles in the event
            for particle in event.particles:
                    if particle.status == 1 and abs(particle.pid) == 13:
                        # Check if the muon is produced by a decaying 2000013 or -2000013 particle
                        #if particle.production_vertex and any(abs(p.pid) == 2000013 for p in particle.production_vertex.particles_in) or any(abs(p.pid) == 13 for p in particle.production_vertex.particles_in):
                            momentum = particle.momentum
                            pt = momentum.pt()
                            hist.Fill(pt)

    # Create a canvas for plotting
    canvas = ROOT.TCanvas("canvas", "Pt Distribution", 800, 600)
    hist.Draw()

    # Customize the plot
    hist.SetTitle("Final Muons Pt Distribution")
    hist.GetXaxis().SetTitle("Pt (GeV)")
    hist.GetYaxis().SetTitle("Number of Events")

    # Display the plot
    canvas.Update()
    ROOT.gROOT.GetListOfCanvases().Draw()
    canvas.SaveAs("pt_plot_non.pdf")

# Specify the path to your HepMC file
hepmc_file = "tag_1_pythia8_events.hepmc"

# Plot the pT distribution
plot_pt_distribution(hepmc_file)
