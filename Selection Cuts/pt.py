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


with hep.open(hepmc_file) as f:
    # Loop over events in the file
    good_event=0
    for event in f:
      leptons=[]
      signal_leptons=[]
      for particle in event.particles:
        if abs(particle.pid) == 13 and particle.status == 1 and particle.momentum.pt()> 65:
          leptons.append(particle)
      
          
      leptons.sort(key=lambda lepton: -lepton.momentum.pt())

        # Select the top two leptons (if there are at least two)
      if len(leptons) >= 2:
        signal_leptons = leptons[:2]
        good_event=good_event+1

        # You can now do something with the signal_leptons, such as analyze them further or store their properties
        # Example: print the pt of the selected leptons
      for lepton in signal_leptons:
        print("Selected lepton pt:", lepton.momentum.pt())
    print(good_event)
          
          
        
           
           
            
           
            
            
            
            
   
