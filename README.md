# EyeCare - Retinal Disease Diagnosis

EyeCare is a desktop application designed to assist ophthalmologists in diagnosing and analyzing retinal diseases using image processing and machine learning techniques. This project provides tools for disease classification, optic disk and optic cup segmentation, and retinal vessel segmentation.

## Abstract
*EyeCare is an advanced desktop application designed to aid
ophthalmologists in diagnosing and analyzing retinal diseases. It leverages
state-of-the-art image processing and machine learning techniques to provide
tools for classifying some of retinal diseases and segmenting the optic disk,
optic cup and retinal vessels. The intuitive interface simplifies the analysis of
retinal fundus images.
Ophthalmic conditions such as diabetic retinopathy, glaucoma, cataract, and
age-related macular degeneration are major causes of global blindness. Early
diagnosis is crucial but challenging due to the labor-intensive nature of manual
evaluations and the expertise required. Artificial intelligence (AI) offers a
solution by enabling automated, precise identification of multiple fundus
pathologies. However, challenges remain due to the presence of multiple
concurrent diseases, scarcity of high-quality images, and image noise.
The application features disease classification, optic disk optic cup
segmentation, and vessel segmentation tools, generating diagnostic reports
that aid in clinical decision-making. Developed with rigorous research and
planning, EyeCare promises contributes to public health by improving access
to advanced diagnostic tools*

## Project Structure
- `/docs/`: Contains project documentation (abstract, chapters, figures).
- `/notebooks/`: Contains Kaggle notebooks for data processing, classification, and segmentation.
- `/data/`: Holds a `README.md` file linking to the datasets used in Kaggle.
- `/results/`: Experimentation results and logs.
- `/GUI/`: Desktop application that use the trained Models .

## Using the Project on Kaggle

### Notebooks
This project is designed to be run in Kaggle Notebooks. You can find the Kaggle Notebooks for each part of the project:

- **Data Processing and Augmentation**: Pre-process and augment the fundus images from the ODIR-5K dataset.
- **Classification**: Train and evaluate the classification models for various retinal diseases.
- **Segmentation**: Perform optic disk, optic cup, and vessel segmentation.

### Kaggle Datasets
To use the notebooks, you need to load the datasets from Kaggle

The datasets are not included in the GitHub repository. Make sure to download or link the datasets in your Kaggle Notebook environment.

## How to Run
1. **Import the Notebooks on Kaggle**: Go to Kaggle and Import the provided notebooks.
2. **Link Datasets**: In each notebook, you can link the Kaggle datasets required for training and testing the models.
3. **Run the Cells**: Execute the cells to preprocess data, train models, and evaluate results.
