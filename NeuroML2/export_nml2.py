from pyneuroml.neuron import export_to_neuroml2

import sys
import os


export_to_neuroml2("load_bc6.hoc", "BC6.cell.nml", includeBiophysicalProperties=False)
