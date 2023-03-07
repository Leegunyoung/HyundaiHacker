import time
import datetime
import cv2
import boto3

rekog = boto3.client('rekognition')
video = cv2.VideoCapture(0)

class VideoCamera(object):

    closed_sec = 0

    def __init__(self):
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        print('camera loaded')

    def __del__(self):
        video.release()

    def get_frame(self):
        # create image frame from video
        success, image = video.read()
        overlay = image.copy()
        h, w = image.shape[:2]
        regImg = cv2.resize(image, (int(0.2 * w), int(0.2 * h)))
        _, newjpeg = cv2.imencode('.jpg', regImg)
        imgbytes = newjpeg.tobytes()
        t0 = time.time()

        # detect eyes details
        resp = rekog.detect_faces(Image={'Bytes': imgbytes}, Attributes=['ALL'])
        try:
            eyes_detail = resp['FaceDetails'][0]['EyesOpen']
        except IndexError:
            eyes_detail = {'Value': False, 'Confidence': 97}

        """add rect behind the status text"""
        # cv2.rectangle(overlay, (10, 10), (200, 50 + 50 * len(eyes_detail)), (0, 0, 0), -1)
        # alpha = 0.3
        # cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        cnt = 1
        now = str(datetime.datetime.now())
        cv2.putText(image, now, (20, 40 * cnt), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cnt += 1

        is_eyes_open = str(eyes_detail['Value'])
        confidence = str(int(eyes_detail['Confidence']))
        outTxt = f"isEyesOpen : {is_eyes_open}({confidence}%)"
        cv2.putText(image, outTxt, (20, 40 * cnt), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

        # encode 'raw images' captured by OpenCV into JPEG to display video stream
        ret, jpeg = cv2.imencode('.jpg', image)

        # 눈을 감고 있는다면
        if is_eyes_open == "False": self.closed_sec += 1
        else: self.closed_sec = 0

        return jpeg.tobytes()
