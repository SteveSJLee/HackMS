from flask import Flask, render_template, Response, redirect, flash, url_for
import json 
import requests
from camera import VideoCamera
import ast

app = Flask(__name__)
app.secret_key = 'mshackathone'

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def capture(camera):
    img = camera.get_frame(capture="y")
    return img

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/takePhoto', methods=['POST'])
def takePhoto():
    url  = "http://dsvm726e4ijbkwrgq.eastus2.cloudapp.azure.com:9999/predict"
    data = {}
    data['img'] = capture(VideoCamera())

    data = json.dumps(data)

    r = requests.post(url, json=data)
    result = ast.literal_eval(r.text)
    print("result", result)
    result = ast.literal_eval(result)
    print("output", result['best'])
    flash(result['best'], 'result')
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
