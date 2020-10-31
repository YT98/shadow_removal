import os

dirname = os.path.dirname(__file__)

silhouettes = os.path.join(dirname, "data/silouhettes")
scans = os.path.join(dirname, "data/scanned_documents")

def directory_image_list(directory):
    list = []
    for filename in os.listdir(directory):
        if (os.path.splitext(filename)[1] == ".jpg"):
            list.append(os.path.join(dirname, directory, filename))
    return list

def get_silhouettes():
    return directory_image_list(silhouettes)

def get_scans():
    return directory_image_list(scans)