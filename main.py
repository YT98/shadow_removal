import os
import sys
import argparse

from shadow_synthesis.ShadowSynthesis import ShadowSynthesis

# Add tools to sys.path so shadow_synthesis directory files can access them
dirname = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dirname, 'tools'))


flags = sys.argv[1:]

help = "--help" in flags
if help:
    print("--training-data: Generate training data.")
    print("--load_masks: Instanciate ShadowSynthesis with existing masks.")
    print("--batches (optional): Define in how many batches training data should be generated. ")

create_training_data = "--training-data" in flags
if create_training_data:
    print("Instanciating ShadowSynthesis...")
    load_masks = "--load-masks" in flags
    shadow_synthesis = ShadowSynthesis(load=load_masks)
    print("ShadowSynthesis successfully instanciated.")

    if "--batches" in flags:
        batches_index = flags.index("--batches")
        batches = int(flags[batches_index + 1])
    else:
        batches = 1
    print("Generating training data ({} batches)...".format(str(batches)))
    shadow_synthesis.create_training_data(batches)
    print("Training data successfully generated.")