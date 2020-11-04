from image_tools import *
from file_tools import *

# from SilhouetteMask import SilhouetteMask
# silhouette = load_image(directory_image_list(ps_he_tb)[0])
# silhouette_mask = SilhouetteMask(silhouette)
# silhouette_mask.scale(1000)
# test_masked = silhouette_mask.apply(test_scan)

# from MaskSet import MaskSet
# scanned_documents = directory_image_list(scanned_documents_path)
# test_scan = load_image(scanned_documents[1])
# mask_set = MaskSet((10,10))
# mask_set.save_masks()
# test_masked = mask_set.apply_masks(test_scan)

# show_image(test_masked)

from ShadowSynthesis import ShadowSynthesis
shadow_synthesis = ShadowSynthesis(load=True)
# shadow_synthesis.mask_set.save_masks()
shadow_synthesis.create_training_data()
