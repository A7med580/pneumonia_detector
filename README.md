# 🫁 PneumoScan AI: Advanced Pneumonia Detection

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**PneumoScan AI** is a state-of-the-art web application that leverages a custom Convolutional Neural Network (CNN) to detect pneumonia from chest X-ray images with high precision.

---

## ✨ Features
- **🚀 AI-Driven Diagnosis**: Powered by a custom CNN achieving **~97.8% training accuracy**.
- **🎨 Premium UI/UX**: Stunning glassmorphism design with fluid animations and responsive layouts.
- **⚡ Real-time Inference**: Lightning-fast predictions delivered via **FastAPI** backend.
- **📁 Smart Upload**: Seamless drag-and-drop interface with instant image preview.
- **🔬 Morphology Analysis**: Advanced analysis pipeline for chest X-ray morphology.

## 📸 Interface Preview
![Interface Preview](/Users/mohamedali/.gemini/antigravity/brain/77473d1e-d83e-4c0b-8f6d-a669a7d098ae/open_web_app_1770129943082.webp)

## 🛠️ Technology Stack
- **Backend**: Python, FastAPI, Uvicorn
- **Machine Learning**: TensorFlow 2.x, Keras, OpenCV, NumPy
- **Frontend**: HTML5, CSS3 (Modern Glassmorphism), Vanilla JavaScript

## 🚀 Getting Started

### 📋 Prerequisites
- **Python 3.10+**
- **pip** (Python package manager)

### 📥 Installation
1. 克隆仓库:
   ```bash
   git clone https://github.com/A7med580/pneumonia_detector.git
   cd pneumonia_detector
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 🏃 Running the Application
1. **Navigate to the App directory**:
   ```bash
   cd app
   ```
2. **Start the server**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. **Explore**:
   Open [http://localhost:8000](http://localhost:8000) in your preferred browser.

## 🧠 Model & Dataset
The CNN model consists of 5 specialized convolutional blocks with BatchNormalization, Dropout, and MaxPooling layers to ensure robust feature extraction and prevent overfitting.

- **Dataset**: [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia)
- **Architecture**: `Sequential` (Conv2D -> BN -> MaxPool -> Dropout)

## 📄 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---
Developed with ❤️ by [Ahmed](https://github.com/A7med580)
