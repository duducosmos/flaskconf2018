from flask import Flask, url_for, render_template
from flask import request, Response, jsonify
import cv2
from facedetection import facedetection
from numpy import array
from camserver import piwebcam

app = Flask(__name__, static_url_path = "", static_folder = "static" )

app.secret_key = 'X456yhj3k510oq'


def gen():    
    
    while True:

        frame  = piwebcam.get_image()
       
        if frame is not None:
            faces = facedetection(piwebcam.get_gray())
            faces = ((x, y, w, h, (255, 0, 0), 2) for (x, y, w, h) in faces)
            for (x, y, w, h, rgb, linewidth) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              rgb, linewidth)
            frame = cv2.imencode('.jpg',frame)[1].tostring()
        else:
            frame = b''
        
        yield (b'--frame\r\n' +
               b'Contetn-Type:image/jpeg\r\n\r\n' +
               frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    piwebcam.setDaemon(True)
    piwebcam.start()
    
    app.run(host="0.0.0.0", port=8080)
    #app.run()
    