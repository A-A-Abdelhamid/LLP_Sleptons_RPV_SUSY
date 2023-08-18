import ROOT
from ROOT import TFile, TGraph2DErrors, gStyle, gROOT, TColor, TLatex
import numpy as np

file_path = "HEPData-ins1831504-v2-pt-d0_muon_efficiency.root"
root_file = TFile.Open(file_path)
directory = root_file.GetDirectory("pt-d0 muon efficiency")
graph = directory.Get("Graph2D_y1")

hist= graph.GetHistogram()
if graph:
    # Get the number of points
    n_points = graph.GetN()

    # Access the data points
    x_values = graph.GetX()
    y_values = graph.GetY()
    z_values = graph.GetZ()

    # Optionally, access the errors
    x_errors = graph.GetEX()
    y_errors = graph.GetEY()
    z_errors = graph.GetEZ()

    # Print the data points
    for i in range(n_points):
        print(f"Point {i}: X = {x_values[i]}, Y = {y_values[i]}, Z = {z_values[i]}")
        print(f"Errors: dX = {x_errors[i]}, dY = {y_errors[i]}, dZ = {z_errors[i]}")
else:
    print("Could not find the object with the name 'Graph2D_y1' in the directory.")
numg= graph.GetN()
num_bins_x = hist.GetNbinsX()
num_bins_y = hist.GetNbinsY()

# Total number of bins including overflow and underflow
total_bins = (num_bins_x + 2) * (num_bins_y + 2)

print("Number of bins along X:", num_bins_x)
print("Number of bins along Y:", num_bins_y)
print("number of points in graph: ", numg)

num_bins_x = hist.GetNbinsX()
num_bins_y = hist.GetNbinsY()
num_bins_z= hist.GetNbinsZ()
# Loop over the bins to get the X and Y values
x_values = [hist.GetXaxis().GetBinCenter(i) for i in range(1, num_bins_x + 1)]
y_values = [hist.GetYaxis().GetBinCenter(i) for i in range(1, num_bins_y + 1)]
z_values = [hist.GetBinContent(5, 9)]

print("x_values :", x_values, " y values: ", y_values," z values: ", z_values)

hist.GetXaxis().SetTitle("Pt (GeV)")

# Set the Y axis label
hist.GetYaxis().SetTitle("d0 (mm)")

# Set the Z axis label (color gradient)
hist.GetZaxis().SetTitle("efficiency")

#f=hist.FindBin(100,25)
#print(f)


print("Total number of bins (including overflow and underflow):", total_bins)
gStyle.SetPalette()
canvas = ROOT.TCanvas("canvas", "2D Histogram")
hist.Draw("colz") # Drawing options can be adjusted as needed
num_bins_x = hist.GetNbinsX()
num_bins_y = hist.GetNbinsY()


canvas.Draw()
canvas.SaveAs("hist.png")
