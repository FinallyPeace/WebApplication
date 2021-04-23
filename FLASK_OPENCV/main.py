import json
from flask import Flask, render_template, request , jsonify, url_for
import numpy as np
import cv2
from flask import make_response
import base64
import os
import datetime
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/', methods=['POST'])
def process():
    file1 = request.files['image1']
    file1_content = file1.read()
    # 將檔案內容轉成 Numpy Array
    # numpy.fromstring(string, dtype=float, count=-1, sep='')
    npImg1 = np.fromstring(file1_content, np.uint8) # unsigned int 0-255
    bgr1 = cv2.imdecode(npImg1, cv2.IMREAD_COLOR) # 預設，以彩色影像讀取， 值為1
    # return jsonify(bgr1.shape)
    
    rgb1 = cv2.cvtColor(bgr1, cv2.COLOR_BGR2RGB)
    height, width = rgb1.shape[:2]
    radius = int(min(height, width) * 0.48)
    thickness = int(min(height, width) * 0.02)
    # cv2.circle(繪圖物件,        (x, y)              , radius,     顏色   , 寬度)
    cv2.circle(rgb1, (int(width / 2), int(height / 2)), radius, (255, 0, 0), thickness)
    bgr1 = cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB)

    # 回傳圖片
    # _var：約定成俗為內部使用 var_：解決命名衝突 __var：private防止子層覆寫
    _, buffer = cv2.imencode('.jpg', bgr1) # _：表示為臨時或無關緊要的變數
    response = make_response(buffer.tobytes())
    response.mimetype = 'image/jpg'

    # 圖片編碼成 Base64 包進 JSON 回傳
    response = {
        'output_image': base64.b64encode(cv2.imencode('.jpg', bgr1)[1]).decode()
    }

    # 存檔並回傳網址
    folderPath = 'static/output_image'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    filename = f'{ datetime.datetime.now().strftime("%Y%m%d_%H%M%S") }.jpg'
    # cv2.imwrite(檔案路徑, 影像物件) -> 用來儲存影像
    cv2.imwrite(os.path.join(folderPath, filename), bgr1)

    response = { # _external=True 告訴Flask要生成絕對url ,而非相對url
        'url': url_for('static', filename = f'output_image/{filename}', _external=True)
    }
    # return response

    # 顯示包含圖片的頁面
    base64_image = base64.b64encode(cv2.imencode('.jpg', bgr1)[1]).decode()

    return render_template('show_image.html', base64_image=base64_image)
'''
@app.route('/', methods=['POST'])
def process():
    file1 = request.files['image1']
    file1_content = file1.read()
    npImg1 = np.fromstring(file1_content, np.uint8)
    bgr1 = cv2.imdecode(npImg1, cv2.IMREAD_COLOR)

    # 取得從 form 來的變數
    line_color_hex = request.form.get('line_color').lstrip('#')
    line_color_rgb = tuple(int(line_color_hex[i:i+2], 16) for i in (0, 2, 4))
    line_thickness = int(request.form.get('line_thickness'))

    # 使用 cv2 處理圖片
    rgb1 = cv2.cvtColor(bgr1, cv2.COLOR_BGR2RGB)
    height, width = rgb1.shape[:2]
    radius = int(min(height, width) * 0.48)
    thickness = int(min(height, width) * 0.01 * line_thickness)
    cv2.circle(rgb1, (int(width/2), int(height/2)), radius, line_color_rgb, thickness)
    bgr1 = cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB)
    
    base64_image = base64.b64encode(cv2.imencode('.jpg', bgr1)[1]).decode()
    return render_template('show_image.html', base64_image=base64_image)
'''