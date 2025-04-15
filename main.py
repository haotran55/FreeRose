from fastapi import FastAPI
from fastapi.responses import JSONResponse
import random

app = FastAPI()

# Danh sách URL ảnh sẵn có
images = [
    "https://files.catbox.moe/it76n1.jpg",
    "https://files.catbox.moe/v2h0ws.jpg",
    "https://files.catbox.moe/eeu6mk.jpg",
    "https://files.catbox.moe/xln7c9.jpg",
    "https://files.catbox.moe/y5htn1.jpg",
    "https://files.catbox.moe/qsuf27.jpg",
    "https://files.catbox.moe/0zj5tk.jpg",
    "https://files.catbox.moe/yigtfg.jpg",
    "https://files.catbox.moe/5vwmk6.jpg",
    "https://files.catbox.moe/w3ygwm.jpg",
    "https://files.catbox.moe/pvicqh.jpg",
    "https://files.catbox.moe/6b8u5h.jpg",
    "https://files.catbox.moe/iixrhj.jpg",
    "https://files.catbox.moe/6b8u5h.jpg",
    "https://files.catbox.moe/8biq07.jpg",
    "https://files.catbox.moe/bve4dc.jpg"
]

@app.get("/")
def root():
    return {"message": "Welcome to Random Image API"}

@app.get("/random-image")
def get_random_image():
    return JSONResponse({"image_url": random.choice(images)})
