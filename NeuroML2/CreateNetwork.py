
import neuroml

import neuroml.loaders as loaders
import neuroml.writers as writers

from pyneuroml.lems import generate_lems_file_for_neuroml


def create_network_for_cell(cell_ref):

    net_ref = "%s_StimNet"%cell_ref
    net_doc = neuroml.NeuroMLDocument(id=net_ref)

    net = neuroml.Network(id=net_ref)
    net_doc.networks.append(net)

    cell_id = '%s_na_k'%cell_ref

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
                                 amplitude='0.5nA')

    net_doc.pulse_generators.append(stim)


    input_list = neuroml.InputList(id="%s_input"%stim.id,
                                   component=stim.id,
                                   populations=pop.id)

    syn_input = neuroml.Input(id=0,
                              target="../%s/0/%s" % (pop.id, pop.component),
                              destination="synapses")

    input_list.input.append(syn_input)
    net.input_lists.append(input_list)



    nml_file = net.id+'.net.nml'

    writers.NeuroMLWriter.write(net_doc,nml_file)

    print("Saved network file to: "+nml_file)


    ###### Validate the NeuroML ######    

    from neuroml.utils import validate_neuroml2

    validate_neuroml2(nml_file)

    sim_id = 'Test'
    target = net.id
    duration=400
    dt = 0.025
    lems_file_name = 'LEMS_%s_%s.xml'%(sim_id,cell_ref)
    target_dir = "."

    interesting_seg_ids = [0,1000,2000,10000]

    to_plot = {'Some_voltages':[]}
    to_save = {'%s_voltages.dat'%cell_id:[]}

    for seg_id in interesting_seg_ids:
        to_plot['Some_voltages'].append('%s/0/%s/%s/v'%(pop.id, pop.component,seg_id))
        to_save['%s_voltages.dat'%cell_id].append('%s/0/%s/%s/v'%(pop.id, pop.component,seg_id))

    generate_lems_file_for_neuroml(sim_id, 
                                   nml_file, 
                                   target, 
                                   duration, 
                                   dt, 
                                   lems_file_name,
                                   target_dir,
                                   gen_plots_for_all_v = False,
                                   plot_all_segments = False,
                                   gen_plots_for_quantities = to_plot,   #  Dict with displays vs lists of quantity paths
                                   gen_saves_for_all_v = False,
                                   save_all_segments = False,
                                   gen_saves_for_quantities = to_save,   #  Dict with file names vs lists of quantity paths
                                   copy_neuroml = False)


if __name__ == "__main__":
    
    create_network_for_cell('BC1')
    create_network_for_cell('BC2')
    create_network_for_cell('BC6')
