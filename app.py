from flask import Flask, render_template, Response
import json 
import requests
from camera import VideoCamera
import ast

app = Flask(__name__)

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
    print('response is\n\n\n\n')

    result = ast.literal_eval(r.text)
    print(result)
    print("type", type(result))
    print(result['best'])
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
