import numpy as np

def calculate_severity(heatmap, disease):
    # No severity for healthy leaf
    if disease in ["Healthy", "HealthyLeaf", "Healthy Leaf"]:
        return "Not Applicable (Healthy)"

    coverage = np.mean(heatmap > 0.5)

    if coverage < 0.2:
        return "Low"
    elif coverage < 0.5:
        return "Medium"
    else:
        return "High"
