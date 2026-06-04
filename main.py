from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import base64
import cv2
import numpy as np

from predictor import predict

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    # Read file content
    contents = await file.read()
    
    # Get predictions
    orig_img, mask, overlay = predict(contents)
    
    # Convert images to base64
    def image_to_base64(img):
        _, buffer = cv2.imencode('.png', img)
        return base64.b64encode(buffer).decode('utf-8')
    
    return JSONResponse({
        "original": image_to_base64(orig_img),
        "mask": image_to_base64(mask),
        "overlay": image_to_base64(overlay)
    })
