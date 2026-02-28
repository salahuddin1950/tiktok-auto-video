from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
import subprocess
import uuid
import os
import random
import google.generativeai as genai

app = FastAPI()

# ====== ตั้งค่า Gemini ======
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# ====== หน้าเว็บ ======
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>AI TikTok Video Generator</title>
    </head>
    <body style="text-align:center;font-family:sans-serif;margin-top:50px;">
        <h1>🚀 AI TikTok Video Generator</h1>
        <form action="/generate" method="post">
            <input type="text" name="product" placeholder="ชื่อสินค้า" required style="width:300px;padding:10px;" />
            <br><br>
            <textarea name="description" placeholder="รายละเอียดสินค้า" required style="width:300px;height:100px;padding:10px;"></textarea>
            <br><br>
            <button type="submit" style="padding:10px 20px;">Generate Video</button>
        </form>
    </body>
    </html>
    """

# ====== สร้างวิดีโอ ======
@app.post("/generate")
async def generate(product: str = Form(...), description: str = Form(...)):

    # --- สุ่ม Hook ---
    hooks = [
        "หยุดก่อน!",
        "บอกเลยว่าตัวนี้กำลังมาแรง!",
        "ใครกำลังมองหาอยู่ต้องดู!",
        "ของมันต้องมี!"
    ]
    hook = random.choice(hooks)

    # --- ให้ Gemini เขียนสคริปต์ ---
    prompt = f"""
    เขียนสคริปต์ขายของสั้น ๆ สำหรับ TikTok ไม่เกิน 15 วินาที
    เริ่มด้วยคำว่า: {hook}
    สินค้า: {product}
    รายละเอียด: {description}
    ปิดท้ายให้กดลิงก์ด้านล่าง
    """

    response = model.generate_content(prompt)
    script = response.text

    filename = str(uuid.uuid4())

    # --- สร้างเสียง (เสียงผู้หญิงน่ารัก) ---
    subprocess.run([
        "edge-tts",
        "--voice", "th-TH-PremwadeeNeural",
        "--text", script,
        "--write-media", f"{filename}.mp3"
    ])

    # --- สร้างวิดีโอพื้นหลังดำ ---
    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=720x1280:d=15",
        "-i", f"{filename}.mp3",
        "-shortest",
        "-c:v", "libx264",
        "-c:a", "aac",
        f"{filename}.mp4"
    ])

    return FileResponse(f"{filename}.mp4", media_type="video/mp4", filename="video.mp4")
