## 4.4 Results and Model Evaluation

To evaluate the segmentation models, we used several key metrics, including Intersection over Union (IoU), Dice coefficient, Precision, Recall, F1-Score, Specificity, and Accuracy. These metrics helped to assess model performance during training, validation, and further evaluation phases.

### Key Metrics:
- **Precision**: Proportion of true positives among all positive predictions, indicating a low false positive rate.
- **Recall**: Proportion of true positives among all actual positives, indicating a low false negative rate.
- **F1-Score**: Harmonic mean of precision and recall, balancing false positives and false negatives.
- **Specificity**: Proportion of true negatives among all actual negatives, indicating a low false positive rate.
- **Accuracy**: Overall proportion of correct predictions.

### 4.4.1 Vessel Segmentation:
The table below summarizes the results from the vessel segmentation experiments.

| Training Scenario                  | Binary IoU | Binary Cross-Entropy Loss | Precision | Recall | F1-Score | Specificity | Accuracy | Data Augmentation | Image Size | Epochs | Validation | Evaluation |
|------------------------------------|------------|---------------------------|-----------|--------|-----------|-------------|----------|------------------|------------|--------|------------|------------|
| U-Net Scratch (256x256)            | 0.7929     | 0.7642                    | 0.4544    | 0.566  | -         | -           | -        | No               | 256        | 200    | -          | -          |
| U-Net Scratch (384x384)            | 0.8029     | 0.8366                    | 0.4144    | 0.2139 | -         | -           | -        | No               | 384        | 200    | -          | -          |
| U-Net + EfficientNetB0             | 0.8647     | 0.8467                    | 0.1776    | 0.1704 | -         | -           | -        | No               | 384        | 150    | -          | -          |
| U-Net + EfficientNetB0             | 0.8599     | 0.8122                    | 0.1576    | 0.1757 | 0.8524    | 0.8324      | 0.8423   | No               | 512        | 150    | -          | -          |
| U-Net + ResNet18                   | 0.8477     | 0.8240                    | 0.1224    | 0.1351 | 0.8498    | 0.8315      | 0.8344   | No               | 512        | 100    | -          | -          |
| U-Net + ResNet-0                   | 0.8644     | 0.8411                    | 0.1597    | 0.2027 | 0.8269    | 0.8397      | 0.8332   | No               | 512        | 150    | -          | -          |
| LinkNet + ResNet50                 | 0.8603     | 0.8348                    | 0.1587    | 0.1917 | 0.8608    | 0.7959      | 0.8271   | No               | 512        | 100    | -          | -          |
| FPNNet + ResNet50                  | 0.8648     | 0.8165                    | 0.1720    | 0.1917 | 0.8618    | 0.8255      | 0.8433   | No               | 512        | 100    | -          | -          |

### 4.4.2 OD & OC Segmentation:
The table below summarizes the results from the OD & OC segmentation experiments.

| Training Scenario                                | Binary IoU | Binary Cross-Entropy Loss | Precision | Recall | F1-Score | Specificity | Accuracy | Data Augmentation | Image Size | Epochs | Validation | Evaluation |
|--------------------------------------------------|------------|---------------------------|-----------|--------|-----------|-------------|----------|------------------|------------|--------|------------|------------|
| U-Net + EfficientNetB0 (Cropped, no preprocessing)| 0.4219     | 0.5854                    | 0.4785    | 0.3889 | 0.8519    | 0.8925      | 0.8645   | No               | 512        | 42     | -          | -          |
| U-Net + EfficientNetB0 (Cropped, preprocessing)   | 0.6434     | 0.4133                    | 0.1223    | 0.3456 | 0.8698    | 0.8966      | 0.8793   | No               | 512        | 50     | -          | -          |
| U-Net + EfficientNetB0 (Full, no preprocessing)   | 0.9536     | 0.9558                    | 0.0144    | 0.013  | 0.8894    | 0.8836      | 0.8881   | No               | 512        | 37     | -          | -          |
| U-Net + EfficientNetB0 (Full, preprocessing)      | 0.9555     | 0.9542                    | 0.0160    | 0.0163 | 0.8980    | 0.8664      | 0.8812   | No               | 512        | 45     | -          | -          |

### Observations:
- **Training Scenario**: U-Net models coupled with EfficientNetB0 (transfer learning) performed significantly better across multiple metrics.
- **Data Augmentation**: Experiments using data augmentation showed improved results for both vessel and OD/OC segmentation.
- **Best Performance**: The U-Net model using EfficientNetB0 with preprocessing achieved the best results, with a Binary IoU of 0.9555 and an Accuracy of 0.9972.
