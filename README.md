# Shadow Removal (Work in Progress)
Training a Convolutional Neural Network (CNN) to detect and remove unwanted shadows from smartphone document captures.

## Data Synthesis

### Silhouettes
A set of manually drawn silhouettes is used to create realistic shadows on a set of document images.

#### Operations on silhouettes:
1. Noise is added to silhouette with a perlin noise mask (see noise module)
2. Silhouette is blurred using a Gaussian convolution operation (see open cv gaussian blurring).
3. Silhouette is randomly scaled (200-500%)
4. Silhouette transparency is randomly determined (0.4 - 0.7)
Silhouette application on document image:
5. Silhouette is padded with empty pixels (or trimmed) so it has same dimensions as document image.
6. Final image is a linear blend between original document image and silhouette image.

| Original silhouette image | Silhouette image after operations | Silhouette image applied on document image |
|---------------------------|-----------------------------------|--------------------------------------------|
|                           |                                   |                                            |

### Document Images
Document images are agregated from two different datasets: [SmartDocQA](http://navidomass.univ-lr.fr/SmartDoc-QA/) from [The IUPR Dataset of Camera-Captured Document Images](https://www.researchgate.net/publication/262294457_The_IUPR_Dataset_of_Camera-Captured_Document_Images). Document images from the IUPR dataset are scanned and trimmed. Document images from SmartDocQA are, they are manually trimmed using open-cv.

#### Operations on SmartDocQA document images:
1. Threshold is applied to blacken part of image which is outside of document (see open cv threshold)
2. Document edges are detected using open cv contour detection.
3. Using document edges, document image is trimmed and warped.

| Original SmartDoc image | SmartDoc image after threshold application | Trimmed SmartDoc image |
|-------------------------|--------------------------------------------|------------------------|
|                         |                                            |                        |

## Neural Network (Coming soon)
