from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)  # อนุญาตให้ HTML เรียก API จากต่าง origin

# EmailJS API - ใส่ค่าจาก dashboard.emailjs.com
# วิธีที่ 1: ตั้งค่า environment variables (แนะนำสำหรับ production)
# วิธีที่ 2: แก้ค่าตรงนี้สำหรับ development
EMAILJS_PUBLIC_KEY = os.environ.get('EMAILJS_PUBLIC_KEY', '')  # เช่น 'abc123xyz'
EMAILJS_SERVICE_ID = os.environ.get('EMAILJS_SERVICE_ID', '')  # เช่น 'service_xxx'
EMAILJS_TEMPLATE_ID = os.environ.get('EMAILJS_TEMPLATE_ID', '')  # เช่น 'template_xxx'

# ฟังก์ชันจำลองข้อมูล PM2.5 (ในอนาคตสามารถเชื่อมต่อกับ API จริงได้)
def get_pm25_level(pm25_value):
    """กำหนดระดับความอันตรายจากค่า PM2.5"""
    if pm25_value <= 25:
        return {'level': 'ดี', 'color': 'good', 'description': 'คุณภาพอากาศดีมาก'}
    elif pm25_value <= 50:
        return {'level': 'ปานกลาง', 'color': 'moderate', 'description': 'คุณภาพอากาศปานกลาง'}
    elif pm25_value <= 100:
        return {'level': 'ไม่ดีต่อสุขภาพ', 'color': 'unhealthy', 'description': 'ไม่ดีต่อสุขภาพสำหรับกลุ่มเสี่ยง'}
    else:
        return {'level': 'ไม่ดี', 'color': 'very-unhealthy', 'description': 'ไม่ดีต่อสุขภาพ'}

# Route สำหรับแสดงหน้า HTML
@app.route('/')
def index():
    return render_template('index.html',
        emailjs_public_key=EMAILJS_PUBLIC_KEY,
        emailjs_service_id=EMAILJS_SERVICE_ID,
        emailjs_template_id=EMAILJS_TEMPLATE_ID
    )

# API endpoint สำหรับข้อมูล PM2.5
@app.route('/api/pm25', methods=['GET'])
def get_pm25():
    # จำลองค่า PM2.5 ที่ระดับสีแดง (101-200) - ในอนาคตสามารถเชื่อมต่อกับ API จริงได้
    pm25_value = random.randint(101, 200)
    level_info = get_pm25_level(pm25_value)
    
    return jsonify({
        'pm25': pm25_value,
        'level': level_info['level'],
        'color': level_info['color'],
        'description': level_info['description'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)

