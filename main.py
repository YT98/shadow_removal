import os
import sys

from shadow_synthesis.ShadowSynthesis import ShadowSynthesis

# Add tools to sys.path so shadow_synthesis directory files can access them
dirname = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dirname, 'tools'))

if __name__ == '__main__':
    flags = sys.argv[1:]

    help = "--help" in flags
    if help:
        print("--training-data: Generate training data.")
        print("--load_masks: Instanciate ShadowSynthesis with existing masks.")

    create_training_data = "--training-data" in flags
    if create_training_data:
        load_masks = "--load-masks" in flags
        shadow_synthesis = ShadowSynthesis(load_masks)
        shadow_synthesis.create_training_data()