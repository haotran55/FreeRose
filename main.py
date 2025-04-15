from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random

app = FastAPI()

# Danh sách URL ảnh sẵn có
images = [
    "https://i.imgur.com/x1.jpg",
    "https://i.imgur.com/x2.jpg",
    "https://i.imgur.com/x3.jpg"
]

@app.get("/")
def root():
    return {"message": "Welcome to Random Image API"}

@app.get("/random-image")
def get_random_image():
    return JSONResponse({"image_url": random.choice(images)})
