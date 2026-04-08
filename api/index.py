from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
import io
import os
import random

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and configuration
# Vercel's working directory is the root of the project
MODEL_PATH = os.path.join(os.getcwd(), 'pneumonia_model.h5')
IMG_SIZE = 150
model = None
MOCK_MODE = False

# Load the model on startup
@app.on_event("startup")
async def startup_event():
    global model, MOCK_MODE
    if os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}. Enabling Mock Mode.")
            MOCK_MODE = True
    else:
        print(f"Model not found at {MODEL_PATH}. Enabling Mock Mode for demo.")
        MOCK_MODE = True

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if MOCK_MODE:
        # Simulate AI processing delay
        import asyncio
        await asyncio.sleep(0.5)
        
        filename = file.filename.lower()
        
        # Deterministic logic for example images to ensure a consistent demo
        if "pneumonia_sample" in filename:
            result = "Pneumonia"
            confidence = random.uniform(94.5, 98.2)
        elif "normal_sample" in filename:
            result = "Normal"
            confidence = random.uniform(96.1, 99.4)
        else:
            # Random logic for user-uploaded images in mock mode
            is_pneumonia = random.random() > 0.6
            result = "Pneumonia" if is_pneumonia else "Normal"
            confidence = random.uniform(82, 95)
        
        return {
            "result": result,
            "confidence": f"{confidence:.2f}%",
            "note": "Prediction generated in Mock Mode (Model file missing)."
        }

    if model is None:
        return JSONResponse(status_code=503, content={"error": "Model not loaded yet."})
    
    try:
        # Read the file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return JSONResponse(status_code=400, content={"error": "Invalid image file."})

        # Preprocess the image
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        img = img.reshape(-1, IMG_SIZE, IMG_SIZE, 3)
        
        # Predict
        prediction = model.predict(img)
        # Using [0][0] because the model output layer is Dense(1, sigmoid)
        confidence_val = float(prediction[0][0])
        
        # Binary classification: 0 = Pneumonia, 1 = Normal (based on train_model.py LABELS order)
        # In train_model.py: LABELS = ['PNEUMONIA', 'NORMAL']
        if confidence_val < 0.5:
            result = "Pneumonia"
            # If 0 is Pneumonia, then 1-val is the confidence of it being pneumonia
            score = (1 - confidence_val) * 100
        else:
            result = "Normal"
            score = confidence_val * 100
            
        return {
            "result": result,
            "confidence": f"{score:.2f}%"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Vercel needs the app object to be named 'app'
