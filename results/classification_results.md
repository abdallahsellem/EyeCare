# Classification Results

### 1. Performance of Backbone Networks on ODIR-5K Dataset

| Model                      | AUC (No Sampling) | F1-Score (No Sampling) | AUC (Oversampling) | F1-Score (Oversampling) |
|----------------------------|-------------------|------------------------|--------------------|-------------------------|
| ResNet-101                  | 70.12             | 78.53                  | 94.33              | 92.28                   |
| ResNet-101 + DKC Block      | 70.26             | 79.28                  | 93.52              | 91.62                   |
| InceptionV3                 | 72.94             | 78.17                  | 86.31              | 87.37                   |
| InceptionV3 + DKC Block     | 73.86             | 79.44                  | 88.59              | 89                      |
| InceptionResNet             | 74.22             | 80.44                  | 94.24              | 91.53                   |
| InceptionResNet + DKC Block | 74.55             | 80.96                  | 95.4               | 92.68                   |

The table shows the improvement in performance when the DKC block is integrated with the backbone networks. Oversampling minority classes during training also resulted in a significant performance increase across all models.

### 2. Comparison with Previous Methods on ODIR-5K Dataset

| Author                    | Method                    | AUC   | F1-Score | Params (M) |
|---------------------------|---------------------------|-------|----------|------------|
| Islam et al., 2019         | Shallow CNN               | 80.5  | 85       | 1.1        |
| Wang et al., 2020          | EfficientNet              | 73    | 88       | -          |
| Gour and Khanna, 2020      | Two Input VGG16           | 84.93 | 85.57    | 15.2       |
| Li et al., 2020            | ResNet-101                | 93    | 91.3     | 74.2       |
| Ning Li et al., 2021       | Inception-v4              | 88    | 85.93    | -          |
| Lin et al., 2022           | Graph Conv. Network       | 78.16 | 89.66    | -          |
| Ou et al., 2022            | ResNet-50                 | 90.3  | 88.6     | 82.6       |
| **Proposed Method**        | InceptionResNet + DKC Block | **94.08** | **92.68** | **96**       |

The proposed method achieved the highest AUC (94.08) and F1-Score (92.68), outperforming previous models tested on the ODIR-5K dataset.

---

## Learning Rate and Optimization Function Impact

| Learning Rate (Initial) | Learning Rate (Final) | Optimizer | Params (M) | AUC  | F1-Score |
|-------------------------|-----------------------|-----------|------------|------|----------|
| 0.001                   | 0.00005               | Adam      | 88.4       | 94.4 | 82.8     |
| 0.0001                  | 0.00005               | Adam      | 88.4       | 95.3 | 85.22    |
| 0.001                   | 0.00001               | SGD       | 88.4       | 86.3 | 80.57    |
| 0.0001                  | 0.00001               | SGD       | 88.4       | 91.8 | 84.19    |
| 0.0001                  | 0.00005               | Adam      | 96.2       | 97.7 | 88.26    |

- **Learning Rate Adjustment**: Lower learning rates (e.g., 0.0001) and gradual reductions in the final learning rate improve model stability and performance, particularly with the Adam optimizer.
- **Optimizer Comparison**: The Adam optimizer consistently outperformed SGD, leading to higher AUC and F1-scores.

---

##   Discussion
The proposed method, DKCNet, significantly improves the classification performance when combined with backbone networks. The use of oversampling for minority classes in training leads to more balanced predictions, resulting in better generalization across diseases.