from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random

app = FastAPI()

# Danh sách URL ảnh sẵn có
images = [
    "https://i.pinimg.com/736x/65/39/30/6539305fb14952972dabefd10d4402b3.jpg",
    "https://anhnail.com/wp-content/uploads/2024/10/Hinh-gai-xinh-k8-cute.jpg",
    "https://1nedrop.com/wp-content/uploads/2024/10/gai-xinh-trung-quoc-57fKByew.jpg"
    "https://tophinhanh.net/wp-content/uploads/2023/12/Hinh-anh-gai-xinh-k8-1.jpg"
]

@app.get("/")
def root():
    return {"message": "Welcome to Random Image API"}

@app.get("/random-image")
def get_random_image():
    return JSONResponse({"image_url": random.choice(images)})
