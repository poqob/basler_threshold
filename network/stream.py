from flask import Flask, Response
import cv2
import pypylon.pylon as py
import numpy as np


app = Flask(__name__)

def get_camera():
  """
  Initializes the camera object and opens the connection.

  Returns:
      py.InstantCamera: The initialized and opened camera object.
  """
  icam = py.InstantCamera(py.TlFactory.GetInstance().CreateFirstDevice())
  icam.Open()
  icam.PixelFormat = "Mono12"
  return icam

cam = get_camera()  # Initialize camera on application startup

def gen_frames():
  while True:
    try:
      image = cam.GrabOne(4000)
      image = image.Array
      ret, jpeg = cv2.imencode(".jpg", image)
      frame = jpeg.tobytes()
      yield (b"--frame\r\n"
             b"Content-Type:image/jpeg\r\n"
             b"Content-Length: "+f"{len(frame)}".encode() + b"\r\n"
             b"\r\n" + frame + b"\r\n")
    except Exception as e:
      print(f"Error capturing frame: {e}")
      break  # Exit the loop on error

@app.route("/")
def index():
    return "Live Video Feed Available"  # More descriptive message

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Use app.run for simpler server management
