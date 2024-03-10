# A Reinterpretation of ["Search for displaced leptons in √s = 13 TeV *pp* collisions with the ATLAS detector"](https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/SUSY-2018-14/)

Our goal is to evaluate the models used by ATLAS with the consideration that they include additional decay modes. 

This project is currently in the intermediate data validation stage. We are recreating the dataset, starting with the  μ̃ → μμ signal region within the 400-500 GeV mass range with a lifetime of 1 ns. 

We are generating collision data via MadGraph as outlined in the [generate_events](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/tree/secondary/generate_events) directory. We ensure the validity of our data with tools contianed in the [event_validation](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/tree/secondary/event_validation) directory, then apply selection cuts via scripts contained in [selection_cuts](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/tree/secondary/selection_cuts). 
