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

def get_final_muon_descendant(particle):
    """
    Get the final state muon descendant of a given particle.

    Parameters
    ----------
    particle : pyhepmc.GenParticle
        The particle to check.
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


with hep.open(hepmc_file) as f:
    # Loop over events in the file
    for event in f:
      for particle in event.particles:
        momentum =particle.momentum
        pt = momentum.pt()
        #All final status muons
        if particle.status == 1 and abs(particle.pid) == 13:
           
            
            histPt.Fill(pt)
            
        # Check if the particle is a muon produced by a decaying 2000013 or -2000013
        if abs(particle.pid) == 13 and particle.production_vertex and any(p.pid in [2000013, -2000013] for p in particle.production_vertex.particles_in):
            # Get the final muon descendant of the muon
            final_muon = get_final_muon_descendant(particle)
            if final_muon is not None:
                histSignalPt.Fill(final_muon.momentum.pt())

canvasPt = ROOT.TCanvas("canvas", "Pt Distribution", 800, 600)
histPt.Draw()
histPt.SetTitle("Final Muons Pt Distribution")
histPt.GetXaxis().SetTitle("Pt (GeV)")
histPt.GetYaxis().SetTitle("Counts")
canvasPt.Update()
canvasPt.SaveAs("pt_plot.pdf")

canvasSigPt = ROOT.TCanvas("canvas", "Signal Pt Distribution", 800, 600)
histSignalPt.Draw()
histSignalPt.SetTitle("Signal Muons Pt Distribution")
histSignalPt.GetXaxis().SetTitle("Pt (GeV)")
histSignalPt.GetYaxis().SetTitle("Counts")
canvasSigPt.Update()
canvasSigPt.SaveAs("Sig_Pt.pdf")
