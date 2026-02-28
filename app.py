from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import subprocess
import uuid

app = FastAPI()

class Product(BaseModel):
    name: str
    description: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>TikTok Auto Video</title>
        </head>
        <body style="text-align:center;font-family:sans-serif;margin-top:50px;">
            <h1>🚀 TikTok Auto Video Generator</h1>
            <p>ระบบออนไลน์แล้ว</p>
        </body>
    </html>
    """

@app.post("/generate")
async def generate_video(product: Product):

    script = f"{product.name} กำลังมาแรงในตอนนี้! {product.description} สนใจดูรายละเอียดเพิ่มเติมที่ลิงก์ด้านล่างเลย"

    filename = str(uuid.uuid4())

    subprocess.run([
        "edge-tts",
        "--text", script,
        "--write-media", f"{filename}.mp3"
    ])

    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=720x1280:d=10",
        "-i", f"{filename}.mp3",
        "-shortest",
        f"{filename}.mp4"
    ])

    return {"video": f"{filename}.mp4"}
