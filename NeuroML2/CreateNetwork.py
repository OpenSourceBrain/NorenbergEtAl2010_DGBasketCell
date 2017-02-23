
import neuroml

import neuroml.loaders as loaders
import neuroml.writers as writers

from pyneuroml.lems import generate_lems_file_for_neuroml

net_ref = "BC_StimNet"
net_doc = neuroml.NeuroMLDocument(id=net_ref)

net = neuroml.Network(id=net_ref)
net_doc.networks.append(net)

cell_id = 'BC2_pas'

net_doc.includes.append(neuroml.IncludeType(cell_id+'.cell.nml')) 

pop = neuroml.Population(id="BC",
            component=cell_id,
            type="populationList")

inst = neuroml.Instance(id="0")
pop.instances.append(inst)
inst.location = neuroml.Location(x=0, y=0, z=0)
net.populations.append(pop)

stim = neuroml.PulseGenerator(id='stim0',
                             delay='50ms',
                             duration='200ms',
                             amplitude='1nA')

net_doc.pulse_generators.append(stim)


input_list = neuroml.InputList(id="%s_input"%stim.id,
                               component=stim.id,
                               populations=pop.id)

syn_input = neuroml.Input(id=0,
                          target="../%s/0/%s" % (pop.id, pop.component),
                          destination="synapses")

input_list.input.append(syn_input)
net.input_lists.append(input_list)



nml_file = net.id+'net.nml'

writers.NeuroMLWriter.write(net_doc,nml_file)

print("Saved network file to: "+nml_file)
  
                                   
###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)

sim_id = 'Test'
target = net.id
duration=400
dt = 0.025
lems_file_name = 'LEMS_%s.xml'%sim_id
target_dir = "."

generate_lems_file_for_neuroml(sim_id, 
                               nml_file, 
                               target, 
                               duration, 
                               dt, 
                               lems_file_name,
                               target_dir,
                               gen_plots_for_all_v = True,
                               plot_all_segments = False,
                               gen_plots_for_quantities = {},   #  Dict with displays vs lists of quantity paths
                               gen_saves_for_all_v = True,
                               save_all_segments = False,
                               gen_saves_for_quantities = {},   #  Dict with file names vs lists of quantity paths
                               copy_neuroml = False)



