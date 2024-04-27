#!/bin/bash
cd $PWD/selection_cuts/
python3 apply_cuts.py
cd ../analysis/
python3 plot_results.py
cd ..
