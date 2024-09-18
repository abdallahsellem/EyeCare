
# Chapter 2: Data Processing and Augmentation - Summary

## 2.4 Data Augmentation in Computer Vision

### 2.4.1 Data Augmentation Based on Labels:
- **Image Augmentation Techniques**: Rotation, scaling, cropping, flipping, translation, noise addition, and color adjustments to generate new images from existing ones.
- **Semantic Segmentation & Object Detection**: Similar techniques applied to models that identify and locate objects within images.

### `dataset_generator_with_augmentation` Function:
- Generates a dataset with data augmentation using a DataFrame of image paths and labels. Techniques are applied based on specific disease labels:
    - **Disease 1 (D)**: Rotation, gamma correction, and original image.
    - **Disease 2 (G)**: Channel shift, flipping, zoom, and rotation.
    - **Disease 3 (C)**: Rotation and flipping.
    - **Disease 4 (A)**: Channel shift, flipping, zoom, rotation, and vertical shift.
    - **Disease 5 (H)**: Channel shift, flipping, zoom, gamma correction, and shifts (vertical and horizontal).

## 2.5 Contrast Limited Adaptive Histogram Equalization (CLAHE)

### 2.5.1 Histogram Equalization:
- Enhances image contrast by redistributing pixel intensities.
- Commonly used in medical imaging to correct under/over-exposed images.

### 2.5.2 Adaptive Histogram Equalization:
- Improves contrast by computing histograms for distinct image sections, preserving local contrast without amplifying noise.

### 2.5.3 CLAHE:
- A variant of adaptive histogram equalization that prevents over-amplification of contrast by operating on image tiles.
- Parameters: 
  - `clipLimit`: Sets threshold for contrast limiting (default: 40).
  - `tileGridSize`: Defines number of tiles for applying CLAHE (default: 8x8).

## 2.6 Hough Transform

### 2.6.1 Overview:
- Detects geometric shapes (lines, circles, ellipses) in images, even when they are incomplete, distorted, or partially obscured.
- Uses voting in parameter space to identify shapes.

### 2.6.2 Algorithm:
1. For each pixel, compute possible curves in parameter space.
2. Increment an accumulator array for each curve.
3. Analyze the array to detect shapes.

### 2.6.3 Advantages:
- Detects geometric shapes under distortion and partial occlusion.
- Invariant to scale, rotation, and translation.
- Efficient and widely applicable in object recognition and other image processing applications.