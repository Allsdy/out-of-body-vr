import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# --- FIX: Add Security Headers to allow VR Textures ---
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Cache-Control'] = 'no-store'
    return response

def generate_frames():
    # Use your iPhone index (2)
    camera = cv2.VideoCapture(2)
    
    # 1. Force High Resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # 2. FORCE 60 FPS (iPhone supports this)
    # Note: If your room is dark, iPhone might auto-drop to 30fps to get more light.
    camera.set(cv2.CAP_PROP_FPS, 60)
    
    # Optional: Remove the internal buffer to reduce latency/old frames
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Mirror logic
            frame = cv2.flip(frame, 1)

            # Reduce JPEG quality slightly to speed up transmission (default is 95)
            # 80 is a good balance for high-speed streaming
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            ret, buffer = cv2.imencode('.jpg', frame, encode_param)
            
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # Ensure you are using the correct port (5001 as you mentioned)
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc', debug=True)