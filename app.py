from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)  # อนุญาตให้ HTML เรียก API จากต่าง origin

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
    return render_template('index.html')

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

