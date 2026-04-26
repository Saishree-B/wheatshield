# 🌾 WheatShield – Explainable Wheat Disease Detection System

## 📌 Overview

WheatShield is a deep learning–based web application designed to detect and classify wheat leaf diseases using image input. The system not only predicts the disease with high accuracy but also provides **confidence, severity level, and actionable recommendations**, along with **Grad-CAM visualizations** for model explainability.

---

## 🚀 Key Features

* 🔐 User Authentication (Register & Login)
* 📸 Image-based wheat disease detection
* 🤖 Deep Learning model (MobileNetV2)
* 📊 Prediction output:

  * Disease type
  * Confidence score
  * Severity level
* 🔥 Grad-CAM visualization for explainability
* 🧾 Recommendation system for treatment
* 📁 History tracking of previous analyses

---

## 🛠️ Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python (Flask)

**Machine Learning**

* TensorFlow / Keras
* MobileNetV2
* OpenCV

**Database**

* SQLite 

---

## 🧠 How It Works

1. User uploads a wheat leaf image
2. Image is sent to the backend
3. Deep learning model predicts disease
4. System returns:

   * Disease label
   * Confidence
   * Severity
   * Recommendation
5. Grad-CAM highlights affected regions
6. Result is stored in history

---

## 📸 Screenshots

### 🔐 User Registration

---

### 🔐 User Login

---

### 🏠 Dashboard

---

### 📤 Prediction Result

---

### 🔥 Grad-CAM Visualization

---

### 📊 Analysis History

---

## 📊 Model Performance

* Test Accuracy: **96.00%**
* Peak Validation Accuracy: **96.80%**
* Final Validation Accuracy: **96.20%**

✔ Consistent performance across training and validation
✔ No overfitting observed

### 🧪 Classification Classes

* BlackPoint
* FusariumFootRot
* HealthyLeaf
* LeafBlight
* WheatBlast

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Saishree-B/wheatshield.git
cd wheatshield
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the application

```bash
python app.py
```

---

## ⚠️ Notes

* Model files are not included due to GitHub size limits
* You can retrain the model using your dataset

---

## 🎯 Future Improvements

* Mobile app integration
* Real-time camera-based detection
* Cloud deployment (AWS / Render)
* Multi-language support for farmers

---

## 👩‍💻 Author

**Sai Shree B**
GitHub: https://github.com/Saishree-B

---

## ⭐ Acknowledgements

* Open-source deep learning libraries
* Agricultural datasets used for training

---

## 💡 Motivation

WheatShield was developed to assist farmers and agricultural experts in **disease detection**, enabling faster intervention and improved crop health using AI.

---
