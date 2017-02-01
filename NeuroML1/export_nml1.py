from pyneuroml.neuron import export_to_neuroml1



#export_to_neuroml2("load_bc6.hoc", "BC6.cell.nml", includeBiophysicalProperties=False)
export_to_neuroml1("load_bc2.hoc", "BC2.nml1", level=1)
