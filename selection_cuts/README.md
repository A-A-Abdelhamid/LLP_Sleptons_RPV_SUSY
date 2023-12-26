The files in this directory are intended to be ran in the following order:
1. (Optional) [efficiency_histogram.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/efficiency_histogram.py)
2. [appy_cuts.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/apply_cuts.py)
3. [plot_results.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/plot_results.py)

# [efficiency_histogram.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/efficiency_histogram.py)
This optional step generates a visualization of the data represented in the [Eff.json](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/Eff.json) file. 

Both were pulled directly from the original paper. The Python script does not have any other effects.

# [appy_cuts.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/apply_cuts.py)
This script applies selection cuts to the generated .hepmc data file. 

In [Line 9 of appy_cuts.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/apply_cuts.py#L9), insert the path to your .hepmc data file. All relevant constants used in selection cuts are listed thereafter in lines 10-15.

Due to a built-in specification in the [Docker image](https://github.com/scailfin/MadGraph5_aMC-NLO/blob/ba3efc64530e192765abd07cd4988f22b075b496/docker/centos/Dockerfile#L44C5-L44C30), momentum units are restricted to MeV. For legibility and ease of alteration, a conversion function is included in our processing file ([lines 42-44](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/apply_cuts.py#L42))and used **only** where absolutely necessary.

The final function of this script is to produce a numpy data file: cut_data.npy. This is a binary file readable only by numpy.load(). For more information, please refer to the documentation for [numpy.save](https://numpy.org/doc/stable/reference/generated/numpy.save.html#numpy.save) and [numpy.load](https://numpy.org/doc/stable/reference/generated/numpy.load.html#numpy.load).

# [plot_results.py](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/blob/secondary/selection_cuts/plot_results.py)
The cut_data.npy file is read in and plotted with ROOT, producing expected.pdf: a single-bin histogram containing all surviving events and a command-line output of the uncertainties and expected SUSY events.

# Results
When you run the python script, this is the output for the 400 GeV 0.1 ns right-handed smuons (with generated number of events = 20,000) with only one decay mode : mur > mu ~ve:

```
Area under the histogram 2241.720458984375
Expected events:  8.134295648868406
```

![image](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/9bda68f6-3d5b-4fde-be54-28ce1799e312)

![image](https://github.com/A-A-Abdelhamid/LLP_Sleptons_RPV_SUSY/assets/130788379/596d2a88-bdb2-49fb-b27e-908b8dcf9993)

