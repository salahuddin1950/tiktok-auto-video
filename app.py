from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
import subprocess
import uuid
import shutil
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="text-align:center;font-family:sans-serif;margin-top:30px;">
    <h2>🔥 AI TikTok Seller 🔥</h2>
    <form action="/generate" method="post" enctype="multipart/form-data">
    <input name="name" placeholder="ชื่อสินค้า" required><br><br>
    <input name="benefits" placeholder="จุดเด่นสินค้า" required><br><br>
    <input type="file" name="image" required><br><br>
    <button type="submit">🚀 สร้างคลิป</button>
    </form>
    </body>
    </html>
    """

@app.post("/generate")
async def generate(
    name: str = Form(...),
    benefits: str = Form(...),
    image: UploadFile = File(...)
):

    uid = str(uuid.uuid4())
    image_path = f"{uid}.jpg"
    audio_path = f"{uid}.mp3"
    video_path = f"{uid}.mp4"

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # 🔥 ให้ AI เขียนสคริปต์ขายของจริง
    prompt = f"""
    เขียนสคริปต์ขายของ TikTok ความยาวไม่เกิน 30 วินาที
    โทนแม่ค้าน่ารัก
    สินค้า: {name}
    จุดเด่น: {benefits}
    ปิดท้ายด้วย Call to Action
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    script = response.choices[0].message.content

    subprocess.run([
        "edge-tts",
        "--voice", "th-TH-PremwadeeNeural",
        "--rate", "+8%",
        "--pitch", "+6Hz",
        "--text", script,
        "--write-media", audio_path
    ])

    subprocess.run([
        "ffmpeg",
        "-loop","1",
        "-i",image_path,
        "-i",audio_path,
        "-shortest",
        video_path
    ])

    return FileResponse(video_path, media_type="video/mp4", filename="tiktok_video.mp4")
