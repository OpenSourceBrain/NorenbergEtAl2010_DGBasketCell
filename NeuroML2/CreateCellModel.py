import neuroml

import neuroml.loaders as loaders
import neuroml.writers as writers

def load_and_rewrite_cell(cell_ref):

    fn = '%s.cell.nml'%cell_ref
    doc = loaders.NeuroMLLoader.load(fn)
    print("Loaded morphology file from: "+fn)

    cell = doc.cells[0]

    axon_seg_group = neuroml.SegmentGroup(id="axon_group",neuro_lex_id="GO:0030424")  # See http://amigo.geneontology.org/amigo/term/GO:0030424
    soma_seg_group = neuroml.SegmentGroup(id="soma_group",neuro_lex_id="GO:0043025")
    dend_seg_group = neuroml.SegmentGroup(id="dendrite_group",neuro_lex_id="GO:0030425")
    inhomogeneous_parameter = neuroml.InhomogeneousParameter(id="PathLengthOverDendrites",variable="p",metric="Path Length from root")
    dend_seg_group.inhomogeneous_parameters.append(inhomogeneous_parameter)

    apic_dend_seg_group = neuroml.SegmentGroup(id="apic_dendrite_group")

    included_sections = []
    for seg in cell.morphology.segments:
        neuron_section_name = seg.name[seg.name.index('_')+1:]

        if not neuron_section_name in included_sections:
            if 'axon' in seg.name:
                axon_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
            elif 'soma' in seg.name:
                soma_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
            elif 'dend' in seg.name:
                dend_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
            elif 'apic' in seg.name:
                dend_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
                apic_dend_seg_group.includes.append(neuroml.Include(segment_groups=neuron_section_name))
            else:
                raise Exception("Segment: %s is not axon, dend or soma!"%seg)

        included_sections.append(neuron_section_name)

    cell.morphology.segment_groups.append(axon_seg_group)
    cell.morphology.segment_groups.append(soma_seg_group)
    cell.morphology.segment_groups.append(dend_seg_group)
    cell.morphology.segment_groups.append(apic_dend_seg_group)

    channel_densities = []
    channel_density_non_uniforms = []

    cd_pas = neuroml.ChannelDensity(id="pas_chan", segment_groups="all", ion="non_specific", ion_channel="pas", erev="-70.0 mV", cond_density="0.021 mS_per_cm2")
    channel_densities.append(cd_pas)

    cd_na = neuroml.ChannelDensity(id="na_chan_soma", segment_groups=soma_seg_group.id, ion="na", ion_channel="Na_BC", erev="55 mV", cond_density="150 mS_per_cm2")
    channel_densities.append(cd_na)


    cdnu_na = neuroml.ChannelDensityNonUniform(id="na_dendrite_group", ion="na", ion_channel="Na_BC", erev="55 mV")
    vp = neuroml.VariableParameter(parameter="condDensity", segment_groups=dend_seg_group.id)
    cdnu_na.variable_parameters.append(vp)
    vp.inhomogeneous_value = neuroml.InhomogeneousValue(inhomogeneous_parameters="PathLengthOverDendrites",value="700 * (H(120-p))") # SI units!!
    channel_density_non_uniforms.append(cdnu_na)

    cd_na = neuroml.ChannelDensity(id="na_chan_axon", segment_groups=axon_seg_group.id, ion="na", ion_channel="Na_BC", erev="55 mV", cond_density="30 mS_per_cm2")
    channel_densities.append(cd_na)

    cd_k = neuroml.ChannelDensity(id="k_chan", segment_groups="all", ion="k", ion_channel="K_BC", erev="-90 mV", cond_density="30 mS_per_cm2")
    channel_densities.append(cd_k)


    specific_capacitances = []

    specific_capacitances.append(neuroml.SpecificCapacitance(value='1.0 uF_per_cm2',
                                                segment_groups='all'))

    init_memb_potentials = [neuroml.InitMembPotential(
        value="-80 mV", segment_groups='all')]

    # 10mV is default for Neuron spike threshold in NetCon
    # https://www.neuron.yale.edu/neuron/static/py_doc/modelspec/programmatic/network/netcon.html
    spike_threshes = [neuroml.SpikeThresh(value="10mV", segment_groups='all')]

    membrane_properties = neuroml.MembraneProperties(
        channel_densities=channel_densities,
        channel_density_non_uniforms = channel_density_non_uniforms,
        specific_capacitances=specific_capacitances,
        init_memb_potentials=init_memb_potentials,
        spike_threshes=spike_threshes)

    # Intracellular Properties
    #
    resistivities = []
    resistivities.append(neuroml.Resistivity(
        value="100 ohm_cm", segment_groups='all'))

    intracellular_properties = neuroml.IntracellularProperties(resistivities=resistivities)

    bp = neuroml.BiophysicalProperties(id="biophys",
                                       intracellular_properties=intracellular_properties,
                                       membrane_properties=membrane_properties)

    cell.biophysical_properties = bp

    cell.id = '%s_na_k'%cell_ref

    nml_doc2 = neuroml.NeuroMLDocument(id=cell.id)

    nml_doc2.includes.append(neuroml.IncludeType('pas.channel.nml')) 
    nml_doc2.includes.append(neuroml.IncludeType('channelConvert/Na_BC.channel.nml')) 
    nml_doc2.includes.append(neuroml.IncludeType('channelConvert/K_BC.channel.nml')) 
    nml_doc2.cells.append(cell)

    nml_file = cell.id+'.cell.nml'

    writers.NeuroMLWriter.write(nml_doc2,nml_file)

    print("Saved the modified morphology file to: "+nml_file)


    ###### Validate the NeuroML ######    

    from neuroml.utils import validate_neuroml2

    validate_neuroml2(nml_file)

if __name__ == "__main__":
    
    load_and_rewrite_cell('BC1')
    load_and_rewrite_cell('BC2')
    load_and_rewrite_cell('BC6')
