from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
import subprocess
import uuid
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>TikTok Auto Video</title>
        </head>
        <body style="text-align:center;font-family:sans-serif;margin-top:50px;">
            <h1>🚀 TikTok Auto Video Generator</h1>
            <form action="/generate" method="post">
                <input type="text" name="name" placeholder="ชื่อสินค้า" required style="width:300px;padding:10px;"><br><br>
                <input type="text" name="description" placeholder="รายละเอียดสินค้า" required style="width:300px;padding:10px;"><br><br>
                <button type="submit" style="padding:10px 20px;">Generate Video</button>
            </form>
        </body>
    </html>
    """

@app.post("/generate")
async def generate_video(name: str = Form(...), description: str = Form(...)):

    script = f"{name} กำลังมาแรงในตอนนี้! {description} สนใจดูรายละเอียดเพิ่มเติมที่ลิงก์ด้านล่างเลย"

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

    return FileResponse(f"{filename}.mp4", media_type="video/mp4", filename="tiktok_video.mp4")
