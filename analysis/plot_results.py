import matplotlib.pyplot as plt
import numpy as np
import uproot
import ROOT
from ROOT import TEfficiency, TFile, TH1F, TGraph2DErrors, gStyle, gROOT, TColor, TLatex

numpy_file = "/eos/home-j/jashley/LLP_Sleptons_RPV_SUSY/selection_cuts/cut_data.npy"
data = np.load(numpy_file)

expected = ROOT.TH1F("Expected","Expected Number of Events",1,0,1)

for value in data:
    expected.Fill(0.5, value)

c = ROOT.TCanvas("canvas", "Expected", 800, 600)
expected.Draw("COLZ")
c.Update()
c.SaveAs("expected.pdf")
area = ( expected.GetSumOfWeights() )

print(f"Area under the histogram (number of surviving events): ", area)
bincontent = expected.GetBinContent(1)
error = expected.GetBinError(1)
print("Bin content: ", bincontent, " error = +/- ", error)
sigma =  0.0005221 * 1000 # 0.5221 fp
L = 139 #1/fb
n_gen = 20000 # # of generated events
print("Expected events: ", (area * sigma * L) / n_gen, "  +/- ",( (error * sigma * L) / n_gen), " events")
