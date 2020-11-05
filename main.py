import os
import sys

from shadow_synthesis.ShadowSynthesis import ShadowSynthesis

# Add tools to sys.path so shadow_synthesis directory files can access them
dirname = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(dirname, 'tools'))

print("Running shadow synthesis")

load = False
while (load != "y" and load != "n"):
    load = input("Would you like to load existing masks? (y/n) ")
    if load == "y":
        print("Creating shadow synthesis instance with existing masks...")
        shadow_synthesis = ShadowSynthesis(load=True)
    elif load == "n":
        print("Creating shadow synthesis instance and creating masks...")
        shadow_synthesis = ShadowSynthesis(load=False)
    else:
        print("Please answer with \"y\" or with \"n\".")
    print("Shadow synthesis successfully instantiated. ")

create_training_data = False
while (create_training_data != "y" and create_training_data != "n"):
    create_training_data = input("Would you like to create training data? (y/n) ")
    if create_training_data == "y":
        batches = int(input("In how many batches would you like to process the training_data creation? "))
        shadow_synthesis.create_training_data(batches)
    elif create_training_data == "n":
        pass
    else:
        print("Please answer with \"y\" or with \"n\".")
