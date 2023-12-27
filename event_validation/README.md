# Code and plots used in validating the events

## Code

### [save_diagrams.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/event_validation/save_diagrams.py)

**Warning: This is a very resource-intensive script. It is recommended only for small data sets.**

This pulls data from your .hepmc file to produce two high-quality vector diagrams (a .pdf and a .svg) for each event. Since runs with many events will result in a very large number of generated diagrams, the code creates and saves all of the files into a subdirectory in the directory in which the code is executed. Unless the string in Line 7 is altered, this subdirectory will be named "event_diagrams."

Please note that Windows users will need to install the PyHepMC package using an alternative to pip. The pip installation method will result in 'unknown format' errors. 

### [single_event_diagram.py]()

If you need to take a closer look at only one of the events in your .hepmc data file, this script allows you to generate a pair of vector files (one .pdf and one .svg) by selecting an event number. To avoid confusion and promote greater potential usefulness, it will also print the following information to the command line:
- The production vertex index number of a previously-specified particle within the event.
- The event record number and the event index number.

Diagrams created by this script will be named "event[specified number]" and saved in the directory in which the script is executed. 

## Plots

### All final status muons

![pt_plot](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/edff8149-7d16-443d-a85b-a9616ed5d6b4)


### By selecting only signal muons (status ==1 and coming from a smuon decay)

![Sig_Pt](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/a180f10f-e07e-4035-87f3-734016352f97)


### One of the events with muons of low pt:

Looking at one of the events an (anti) muon with status ==1 but not produced by a smuon decay:

![Screenshot 2023-07-19 10 42 35 AM](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/052ff872-891c-47bc-9833-fb08bd76024b)


It is produced by a meson decay, its pt is ~ 1 GeV, total energy of ~12 GeV


### All unexpected particles come from photon interactions, here is an event of them I looked at:


![image](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/1c7e42fa-ddce-4cac-a6d8-78346b7997d4)


## Eta plots for all final muons and for signal muons


![Eta](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/cf766e54-a301-443e-ad9b-393657e793ba)






![Sig_Eta](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/dc1b0c9b-d7f2-4131-b1a7-e55f3471614e)




