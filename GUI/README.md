
# EyeCare Application

## Overview

The EyeCare application is a GUI-based tool for analyzing medical images, particularly eye images, to assist in detecting diseases such as diabetic retinopathy, glaucoma, and others. The app offers functionality for both classification and segmentation of medical images, utilizing machine learning models for accurate results.

## Features

- **Classification**: Identifies diseases based on the provided eye images.
- **Optic Disk Segmentation**: Segments the optic disk from the eye images.
- **Vessel Segmentation**: Segments blood vessels from the eye images.
- **Image Enhancement**: Uses CLAHE, brightness enhancement, and gamma correction to preprocess images for improved model accuracy.

## File Descriptions

### `main.py`

- This file contains the logic for loading models and performing predictions on textual descriptions.
- Utilizes `TensorFlow` and `transformers` to tokenize text inputs and predict both priority and assigned team based on a provided description.
  
#### Key Functions:
- `tokenize_texts`: Tokenizes text input using XLNet.
- `load_and_predict`: Loads a pre-trained model and makes predictions based on tokenized text.

### `classification.py`

- This file provides image processing utilities, including image loading, resizing, cropping, and contrast enhancement.
- Implements multi-threading for parallel model loading.

#### Key Functions:
- `loadImg`: Loads an image and converts it to a NumPy array.
- `resizeImg`: Resizes images to fit the desired aspect ratio while maintaining a consistent size.
- `crop`: Detects circular contours in the image and crops them.
- `enhanceImg`: Enhances image contrast using CLAHE for better model prediction accuracy.

### `segmentation.py`

- Contains several image processing functions for contour detection, brightness enhancement, CLAHE, and gamma correction. These preprocessing techniques are applied to improve the quality of images before segmentation.
  
#### Key Functions:
- `find_contours`: Detects and processes contours in binary masks.
- `crop_contours`: Crops an image based on detected contours.
- `apply_clahe`: Applies CLAHE for contrast enhancement.
- `brightness_enhancement`: Enhances brightness in the image.
- `gamma_correction`: Applies gamma correction to the image.
- `read_image_with_preprocess`: Reads and preprocesses images by resizing, applying CLAHE, brightness enhancement, and gamma correction.

### `GUI.py`

- The main graphical interface of the EyeCare application, built using `customtkinter` for a modern and user-friendly experience.
- Provides drag-and-drop functionality for image uploads and displays results in a well-structured interface.
  
#### Key Features:
- Drag & Drop support for image uploads.
- Handles classification and segmentation tasks via buttons in the GUI.
- Displays both the original and segmented images.
- Offers the ability to print a report of the classification and segmentation results.

## Requirements

- Python 3.x
- Required packages are listed below:
  - `tensorflow`
  - `customtkinter`
  - `Pillow`
  - `transformers`
  - `opencv-python`
  - `segmentation_models`
  - `reportlab`



## How to Run

1. Clone the repository.
2. Ensure all dependencies are installed using the above command.
3. Run the `GUI.py` file to launch the EyeCare application.

```bash
python GUI.py
```

## Usage

- **Classification**: Upload an eye image, and the app will predict possible diseases.
- **Optic Disk Segmentation**: Perform segmentation of the optic disk.
- **Vessel Segmentation**: Perform segmentation of blood vessels.
- **Image Enhancement**: The app preprocesses images for better results.
