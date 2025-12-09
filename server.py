import cv2
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)

# --- 全局视口状态 ---
view_state = {
    'x': 0.5,
    'y': 0.5
}

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/control', methods=['POST'])
def control_view():
    """直接接收前端计算好的精确坐标"""
    data = request.json
    global view_state
    
    # 前端现在负责计算平滑度，直接把坐标传过来即可
    if 'x' in data:
        view_state['x'] = max(0.0, min(1.0, float(data['x'])))
    if 'y' in data:
        view_state['y'] = max(0.0, min(1.0, float(data['y'])))
        
    return jsonify(view_state)

def generate_frames():
    # 使用你之前测试成功的 Index (例如 2)
    camera = cv2.VideoCapture(2)
    
    # 强制高分辨率和高帧率
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 60)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)

            # --- 动态裁切逻辑 (和之前一样，但坐标源变平滑了) ---
            h, w = frame.shape[:2]
            crop_w = int(w * 0.5)
            crop_h = int(h * 0.5)
            
            max_x_offset = w - crop_w
            max_y_offset = h - crop_h
            
            # 使用全局平滑坐标
            start_x = int(view_state['x'] * max_x_offset)
            start_y = int(view_state['y'] * max_y_offset)
            
            # 边界安全检查
            start_x = max(0, min(start_x, w - crop_w))
            start_y = max(0, min(start_y, h - crop_h))
            
            end_x = start_x + crop_w
            end_y = start_y + crop_h

            cropped_frame = frame[start_y:end_y, start_x:end_x]
            frame = cv2.resize(cropped_frame, (w, h), interpolation=cv2.INTER_LINEAR)
            
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            ret, buffer = cv2.imencode('.jpg', frame, encode_param)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc', debug=True)