from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
import cv2
import io
import os

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
MODEL_PATH = '../pneumonia_model.h5'
IMG_SIZE = 150
model = None

# Load the model on startup
@app.on_event("startup")
async def startup_event():
    global model
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print(f"Model not found at {MODEL_PATH}. Prediction will not work until training is complete.")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse(status_code=503, content={"error": "Model not loaded yet. Please wait for training to finish."})
    
    try:
        # Read the file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Preprocess the image
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img / 255.0
        img = img.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
        
        # Predict
        prediction = model.predict(img)
        confidence = float(prediction[0][0])
        
        # Binary classification: 0 = Pneumonia, 1 = Normal (Based on our training script labels)
        # Note: In our training script, LABELS = ['PNEUMONIA', 'NORMAL']
        # prediction[0][0] is the probability of class 1 ('NORMAL')
        
        if confidence < 0.5:
            result = "Pneumonia"
            score = (1 - confidence) * 100
        else:
            result = "Normal"
            score = confidence * 100
            
        return {
            "result": result,
            "confidence": f"{score:.2f}%"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Mount the static files directory
app.mount("/", StaticFiles(directory="static", html=True), name="static")
