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
from ROOT import TEfficiency, TFile, TH1F


   
total_histogram = TH1F()
passed_histogram = TH1F()

# Fill the histograms with total events and passed events
p = 7856     # Number of passed events (numerator)

n= 20000-p

p_err= math.sqrt(p)
n_err= math.sqrt(n)

dA_dp= n/((n+p)**2)
dA_dn= p/((n+p)**2)

sigma_A= math.sqrt((dA_dp*p_err)**2 + (dA_dn*n_err)**2 )

A= p/(p+n)
print("Acceptance is: ", A, "with uncertainty of ", sigma_A)

   
           
           
            

            
            
            
            
   
