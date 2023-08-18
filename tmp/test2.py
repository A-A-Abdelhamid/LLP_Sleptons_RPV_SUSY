import ROOT
from ROOT import TFile, TGraph2DErrors, gStyle, gROOT, TColor, TLatex
import numpy as np

file_path = "HEPData-ins1831504-v2-pt-d0_muon_efficiency.root"
root_file = TFile.Open(file_path)
directory = root_file.GetDirectory("pt-d0 muon efficiency")
graph = directory.Get("Graph2D_y1")

npoints = graph.GetN()
hist = ROOT.TH2F()
x=graph.GetX()
z=graph.GetZ()
y=graph.GetY()
for i in range(npoints):
    xc=x[i]
    yc=y[i]
    zc=z[i]
    hist.Fill(xc, yc, zc)  # Here z is used as the weight for the bin
canvas = ROOT.TCanvas("canvas", "2D Histogram")
# Draw the histogram
hist.Draw("COLZ")

canvas.Draw()
canvas.SaveAs("hist2.png")
