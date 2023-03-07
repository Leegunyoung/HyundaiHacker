from flask import Flask, render_template, Response, redirect, url_for
# from selenium import webdriver
from camera import VideoCamera
import requests

app = Flask(__name__)
called = False

# driver = webdriver.Chrome("C:/Users/김진영/Downloads/chromedriver_win32")
# url = "http://127.0.0.1:5000"
# driver.get(url)

@app.route('/')
def index():
    global called
    if called == False:
        called = True
        # response.headers['Cache-Control'] = 'no-store'
        return render_template('index.html')
    else:
        # response.headers['Cache-Control'] = 'no-store'
        return render_template('indexAndMap.html')

def index():
    called = getattr(index, 'called', False)
    if called == False:
        index.called = True
        return render_template('index.html')
    else:
        return render_template('indexAndMap.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        eyes_csd_sec = camera.closed_sec
        if eyes_csd_sec >= 3:
            call_phone()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def findmap():
    # driver.refresh()
    return redirect(url_for('index'))

"""if camera spot driver is now sleeping, call the phone and give the safe destination location data."""
# @app.route('/api/data')

def call_phone():
    api_endpoint = "https://tl9b7wjalf.execute-api.ap-northeast-2.amazonaws.com/default/helloc"
    response = requests.get(api_endpoint)
    findmap()

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 'Error: unable to retrieve data from API'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)