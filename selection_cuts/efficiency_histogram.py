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
hist = ROOT.TH2F("hist", "hist",10, 65, 765, 8, 0, 400)
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
    Pt.append( float( entry['x'][0]['value'] ) )
    d0.append( float( entry['x'][1]['value'] ) )
    eff.append( float( entry['y'][0]['value'] ) )

# Fill the histogram
for i in range( len(Pt) ):
    # Adding 1 to ensure we start from bin 1 ### TODO Is something missing here?
    x_bin = hist.GetXaxis().FindBin( Pt[i] )
    y_bin = hist.GetYaxis().FindBin( d0[i] )
    hist.SetBinContent( x_bin, y_bin, eff[i] )

# Draw the histogram
cH = ROOT.TCanvas("canvasH", "Pt-do eff", 800, 600)
hist.GetXaxis().SetTitle("Pt (GeV)")
hist.GetYaxis().SetTitle("d0 (mm)")
hist.SetTitle("Muon reconstruction efficiency")
hist.Draw("COLZ")
cH.Update()

