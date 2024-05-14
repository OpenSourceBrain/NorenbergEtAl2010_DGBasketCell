#!/bin/bash
set -ex

python export_nml2.py 
python CreateCellModel.py
python CreateNetwork.py  

omv all -V 
