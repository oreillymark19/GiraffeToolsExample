#This is a Nipype generator. Warning, here be dragons.
#!/usr/bin/env python

import sys
import nipype
import nipype.pipeline as pe

import nipype.interfaces.io as io
import nipype.interfaces.fsl as fsl

#Generic datasink module to store structured outputs
io_data_sink = pe.Node(interface = io.DataSink(), name='io_data_sink')
io_data_sink.inputs.base_directory = /mnt/Data/Stuff

#Flexibly collect data from disk to feed into workflows.
io_select_files = pe.Node(io.SelectFiles(templates={}), name='io_select_files', iterfield = ['sub_ID'])
io_select_files.iterables = [('sub_ID', ['01','02','03'])]

#Wraps the executable command ``fslroi``.
fsl_extract_roi = pe.MapNode(interface = fsl.ExtractROI(), name='fsl_extract_roi', iterfield = ['in_file'])

#Wraps the executable command ``bet``.
fsl_bet = pe.Node(interface = fsl.BET(), name='fsl_bet')

#Wraps the executable command ``flirt``.
fsl_flirt = pe.Node(interface = fsl.FLIRT(), name='fsl_flirt')

#Create a workflow to connect all those nodes
analysisflow = nipype.Workflow('MyWorkflow')
analysisflow.connect(io_select_files, "func", fsl_extract_roi, "in_file")
analysisflow.connect(io_select_files, "anat", fsl_bet, "in_file")
analysisflow.connect(fsl_extract_roi, "roi_file", fsl_flirt, "in_file")
analysisflow.connect(fsl_bet, "out_file", fsl_flirt, "reference")
analysisflow.connect(fsl_flirt, "out_matrix_file", io_data_sink, "registration")
analysisflow.connect(fsl_bet, "out_file", io_data_sink, "skull_stripped")

#Run the workflow
plugin = 'MultiProc' #adjust your desired plugin here
plugin_args = {'n_procs': 1} #adjust to your number of cores
analysisflow.write_graph(graph2use='flat', format='png', simple_form=False)
analysisflow.run(plugin=plugin, plugin_args=plugin_args)
