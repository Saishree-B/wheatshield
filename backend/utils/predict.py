import numpy as np

def predict_disease(model, img, idx_to_class):
    pred = model.predict(img)
    class_id = int(np.argmax(pred[0]))
    confidence = float(np.max(pred[0]))
    disease = idx_to_class[class_id]
    return disease, confidence
