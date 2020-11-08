import os
import cv2

# Directory paths
dirname = os.path.join(os.path.dirname(__file__), "../")
data = os.path.join(dirname, "data")
# Mask paths
# ps - phone silhouettes
# se, he - soft edges, hard edges
# tb, wb - transparent background, white background
ps_path = os.path.join(dirname, "data/phone_silhouettes")
ps_he_tb = os.path.join(ps_path, "hard_edges/trans_bg")
ps_he_wb = os.path.join(ps_path, "hard_edges/white_bg")
ps_se_tb = os.path.join(ps_path, "soft_edges/trans_bg")
ps_se_wb = os.path.join(ps_path, "soft_edges/white_bg")
perlin_masks_path = os.path.join(data, "masks/perlin_masks")
silhouette_masks_path = os.path.join(data, "masks/silhouette_masks")
# Document paths
scanned_documents_path = os.path.join(data, "scanned_documents/grayscale")
# hard_drive_path = "/Volumes/UNTITLED/"
# smart_doc_documents_path = os.path.join(hard_drive_path, "smart_doc_documents")
smart_doc_documents_path = os.path.join(data, "smart_doc_documents")
# Training data paths
training_data_path = os.path.join(data, "training_data")

# Returns list of png or jpg files in directory
def directory_image_list(directory):
    list = []
    for filename in os.listdir(directory):
        if (os.path.splitext(filename)[1] == ".jpg" or os.path.splitext(filename)[1] == ".png") and not filename.startswith('.'):
            list.append(os.path.join(dirname, directory, filename))
    return list

# Renames all files in directory with name and number
def rename_files(directory, name):
    for count, filename in enumerate(os.listdir(directory)):
        ext = os.path.splitext(filename)[1]
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, name + str(count) + ext)
        os.rename(src, dst)

# Saves image to destination
def save_image(destination, image):
    cv2.imwrite(destination, image)
