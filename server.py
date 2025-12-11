import cv2
from flask import Flask, render_template, Response, request, jsonify
import pygame 
import os

app = Flask(__name__)

# ==========================================
# 1. 音频系统初始化
# ==========================================
try:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(32) 
    print("✅ Pygame Audio Mixer Initialized")
except Exception as e:
    print(f"❌ Audio Init Failed: {e}")

sounds = {}
memory_sounds = {} 

def load_sounds():
    try:
        sounds['heartbeat'] = pygame.mixer.Sound('static/heartbeat.mp3')
        sounds['flatline']  = pygame.mixer.Sound('static/flatline.mp3')
        sounds['underwater'] = pygame.mixer.Sound('static/underwater_muffled.mp3')
        sounds['footstep'] = pygame.mixer.Sound('static/footstep.mp3')
        sounds['injection'] = pygame.mixer.Sound('static/injection.mp3')
        sounds['defibrillator'] = pygame.mixer.Sound('static/defibrillator.mp3')

        for i in range(1, 11):
            filename = f'static/mem/{i}.mp3'
            if not os.path.exists(filename): filename = f'static/mem{i}.mp3'
            if os.path.exists(filename):
                memory_sounds[i] = pygame.mixer.Sound(filename)
                memory_sounds[i].set_volume(1.0) 
        
        # 初始状态
        sounds['underwater'].set_volume(0.0)
        sounds['underwater'].play(loops=-1)
        sounds['heartbeat'].set_volume(1.0)
        
        print("✅ Sounds loaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not load sound files. Details: {e}")

load_sounds()

# ==========================================
# 2. 视口控制
# ==========================================
view_state = {'x': 0.6, 'y': 0.5}

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/control', methods=['POST'])
def control_view():
    data = request.json
    global view_state
    if 'x' in data: view_state['x'] = max(0.0, min(1.0, float(data['x'])))
    if 'y' in data: view_state['y'] = max(0.0, min(1.0, float(data['y'])))
    return jsonify(view_state)

# ==========================================
# 3. 视频流逻辑
# ==========================================
def generate_frames():
    camera = cv2.VideoCapture(3)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 60)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:
        success, frame = camera.read()
        if not success: break
        else:
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            crop_w, crop_h = int(w * 0.8), int(h * 0.8)
            max_x, max_y = w - crop_w, h - crop_h
            sx = int(view_state['x'] * max_x)
            sy = int(view_state['y'] * max_y)
            sx = max(0, min(sx, max_x))
            sy = max(0, min(sy, max_y))
            cropped = frame[sy:sy+crop_h, sx:sx+crop_w]
            frame = cv2.resize(cropped, (w, h), interpolation=cv2.INTER_LINEAR)
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# ==========================================
# 4. 路由定义
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --- 音效控制 ---
@app.route('/trigger_effect', methods=['POST'])
def trigger_effect():
    data = request.json
    action = data.get('action')
    
    if 'heartbeat' not in sounds:
        return jsonify({"status": "error", "msg": "Sounds not loaded"})

    def stop_memories():
        for s in memory_sounds.values(): s.stop()

    # 1. 现实 -> 走马灯
    if action == 'mode_review':
        sounds['heartbeat'].fadeout(3000) 
        sounds['underwater'].set_volume(0.4) 
        stop_memories()

    # 2. 走马灯 -> OBE
    elif action == 'mode_obe':
        sounds['underwater'].set_volume(1.0) 
        # 双重保险：确保回忆声音完全停止
        stop_memories()
    
    # 3. OBE -> 现实
    elif action == 'mode_reality':
        sounds['underwater'].set_volume(0.0)
        sounds['heartbeat'].play(loops=1, fade_ms=200) 
        stop_memories()

        # [新增] 记忆洪流：所有记忆声音渐入
    elif action == 'flood_memories':
        for s in memory_sounds.values():
            # 随机音量稍微不同，增加混乱感
            s.set_volume(0.6) 
            s.play(loops=0, fade_ms=4000) # 4秒内渐入
    
    # [新增]：转场期间淡出回忆
    # 当用户按下按钮准备离开 Life Review 时触发
    elif action == 'fade_memories':
        # 遍历所有回忆音效，执行 4秒 的淡出
        # 这样在屏幕完全变黑前声音就会消失
        for s in memory_sounds.values():
            s.fadeout(4000)

    elif action == 'play_footstep':
        if 'footstep' in sounds:
            # 渐入脚步声 (1秒)
            sounds['footstep'].play(fade_ms=1000)
            
    elif action == 'play_injection':
        if 'injection' in sounds:
            sounds['injection'].play()

    elif action == 'play_flatline':
        if 'flatline' in sounds:
            sounds['flatline'].play()

    # 其他音效
    elif action == 'play_defibrillator':
        if 'defibrillator' in sounds: 
            sounds['defibrillator'].play(loops=1, fade_ms=3000)

    elif action == 'play_heartbeat_transition':
         sounds['heartbeat'].play(loops=2, fade_ms=500)
         
    elif action == 'focus_enter':
        img_id = data.get('id')
        if img_id in memory_sounds:
            memory_sounds[img_id].play(loops=-1, fade_ms=1000)
            
    elif action == 'focus_exit':
        img_id = data.get('id')
        if img_id in memory_sounds:
            memory_sounds[img_id].fadeout(3000)

    return jsonify({"status": "ok", "action": action})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc', debug=False)