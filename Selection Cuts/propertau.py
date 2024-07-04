import matplotlib.pyplot as plt
import numpy as np
import pyhepmc as hep
import pyhepmc.io as ihep
import pyhepmc.view as vhep
import csv
import uproot
import ROOT

filename = "tag_1_pythia8_events.hepmc"

reader=ihep.ReaderAsciiHepMC2(filename)

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
  



def CalcD0(particle):
 

    ver = particle.production_vertex.position
    vx = ver.x
    vy = ver.y
    #vz = ver.z

    momentum = particle.momentum
    px = momentum.px
    py = momentum.py
    #pz = momentum.pz

    # Calculate transverse position vector
    v0_xy = ROOT.TVector3(vx, vy, 0)
    v0_xy_Mag = (vx**2 + vy**2)**0.5
    # Calculate transverse momentum vector
    p_xy = ROOT.TVector3(px, py, 0)

    # Calculate delta phi directly
    d_phi = ROOT.TVector2.Phi_mpi_pi(p_xy.DeltaPhi(v0_xy))

    # Calculate transfer impact parameter using L_xy * sin(phi)
    transfer_impact_parameter = v0_xy_Mag * ROOT.TMath.Sin(d_phi)

    return transfer_impact_parameter


def CalcPhi(particle):

  momentum =particle.momentum
  px=momentum.px
  py=momentum.py
  phi = np.arctan2(py, px)
  return phi
 
 
hist = ROOT.TH1F("tau0_distribution", "Proper Lifetime Distribution", 100,0, 50)

def plot_pt_distribution(hepmc_file):
    # Create a histogram to store the pT distribution
    
 
    # Open the HepMC file
    with hep.open(hepmc_file) as infile:
        i=0
        for event in infile:
               
                for vertex in event.vertices:
                    for mparticle in vertex.particles_in:
                      if mparticle.pid == -2000013 or mparticle.pid == 2000013:
                        momentum = mparticle.momentum
                        mass= mparticle.generated_mass
                        energy= momentum.e
                        gamma= (energy/mass)
                        for dparticle in vertex.particles_out:
                        # Fill the histogram with the pT of each particle
                          if dparticle.pid == 13 or dparticle.pid == -13:
                            
                           # pt = momentum.pt()
                          # time=particle.production_vertex
                          #  parent=particle.parents
                          #  parentevent=particle.parent_event
                            
                           # s=momentum.interval()
                            #T =momentum.t
                            pos=vertex.position
                            Tpos= pos.t
                            
                            #hbar = 6.582119569e-25
                            #lifetime= energy
                            #if Tpos >= 3 and Tpos <=300:
                              
                            lifetime= 1E9*(Tpos/(3E11))
                            proper=lifetime/gamma
                            hist.Fill(proper)

                            
    
    # Create a canvas for plotting
    canvas = ROOT.TCanvas("canvas", "Proper Lifetime Distribution", 800, 600)
    hist.Draw()

    # Customize the plot
    hist.SetTitle("Tau0 Distribution")
    hist.GetXaxis().SetTitle("Tau [ns]")
    hist.GetYaxis().SetTitle("Number of Events")
  

    # Display the plot
    canvas.Draw()
    canvas.Update()
    
    canvas.SaveAs("proper_time.pdf")

# Specify the path to your HepMC file
hepmc_file = "tag_1_pythia8_events.hepmc"

# Plot the pT distribution
plot_pt_distribution(hepmc_file)

# Define exponential function
def exponential(x, par):
    return par[0] * ROOT.TMath.Exp(-par[1] * x[0])
    
fit_function = ROOT.TF1("fit_function", exponential, 400, 10, 2)  # 2 parameters: amplitude and decay constant

# Set initial parameter values for the fit
fit_function.SetParameters(400, 10)  # Example initial parameter values

# Perform fit
fit_result = hist.Fit(fit_function, "S")

# Access fit results
amplitude = fit_function.GetParameter(0)
decay_constant = fit_function.GetParameter(1)

# Create legend and add fit equation
legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
legend.AddEntry(hist, "Histogram", "l")
legend.AddEntry(fit_function, "Fit: %.2f * exp(-%.2f * x)" % (amplitude, decay_constant), "l")

# Print fit results
print("Fit Amplitude:", amplitude)
print("Fit Decay Constant:", decay_constant)

# Draw histogram and fit function
canvasf = ROOT.TCanvas("canvasf", "Exponential Fit", 800, 600)
hist.Draw()
fit_function.Draw("same")
#legend.Draw()
canvasf.Draw()
canvasf.SaveAs("proper_time_fit_300.pdf")

   

      

