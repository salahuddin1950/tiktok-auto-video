from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse
import subprocess
import uuid
import random
import shutil

app = FastAPI()

# 🔥 Hook เปิดคลิป
hooks = [
"หยุดก่อน! ตัวนี้กำลังไวรัลมาก 🔥",
"ใครกำลังมองหาของดีราคาคุ้ม ต้องดูอันนี้เลย",
"เตือนแล้วนะ เดี๋ยวของหมด!",
"ไม่ซื้อวันนี้อาจพลาดของดีไปเลย",
"ตัวนี้กำลังมาแรงสุด ๆ ในตอนนี้"
]

# 🔥 Call to Action ปิดท้าย
ctas = [
"กดดูรายละเอียดที่ลิงก์ด้านล่างเลยนะคะ 💕",
"สนใจกดสั่งซื้อได้เลยค่ะ 🔥",
"ของมีจำนวนจำกัด รีบเลยนะคะ",
"ช้าหมด อดนะคะ!",
"กดตะกร้าได้เลยตอนนี้"
]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="text-align:center;font-family:sans-serif;margin-top:30px;">
    <h2>🔥 TikTok Auto Seller Step 1 🔥</h2>
    <form action="/generate" method="post" enctype="multipart/form-data">
    <input name="name" placeholder="ชื่อสินค้า" required><br><br>
    <input name="benefits" placeholder="จุดเด่นสินค้า (คั่นด้วย , )" required><br><br>
    <input type="number" name="count" value="3" min="1" max="10"><br><br>
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
    count: int = Form(...),
    image: UploadFile = File(...)
):

    benefit_text = benefits.replace(",", " ")

    for i in range(count):

        uid = str(uuid.uuid4())
        image_path = f"{uid}.jpg"
        audio_path = f"{uid}.mp3"
        video_path = f"{uid}.mp4"

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        hook = random.choice(hooks)
        cta = random.choice(ctas)

        script = f"""
        {hook}
        วันนี้มาแนะนำ {name}
        จุดเด่นคือ {benefit_text}
        {cta}
        """

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

    return {"status": f"สร้าง {count} คลิปเรียบร้อย"}
