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
    # Use the index that worked (e.g., 1)
    camera = cv2.VideoCapture(2) 
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # --- NEW LINE: Mirror the image (1 = Horizontal Flip) ---
            frame = cv2.flip(frame, 1)

            ret, buffer = cv2.imencode('.jpg', frame)
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