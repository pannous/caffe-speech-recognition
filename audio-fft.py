#!/usr/bin/env python

import pyaudio
# import wave

import subprocess
import re
import flask
import werkzeug
import optparse
import tornado.wsgi
import tornado.httpserver
from flask.ext.cors import CORS # Access-Control-Allow-Origin
import skimage.io
import json
import traceback
# import opencv2
import cv2
import cv
import numpy
import os
import sys
from os import system
from platform import system as platform
import skimage.io

winName="Server"
cv2.namedWindow(winName, cv.CV_WINDOW_FULLSCREEN)
if platform() == 'Darwin':  # How Mac OS X is identified by Python
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')


# Obtain the flask app object
app = flask.Flask(__name__)
cors = CORS(app)

i = 0
image=numpy.array(bytearray(os.urandom(512*512))) # 512,512)
image=image.reshape(512,512)

@app.route('/')
def index():
# return flask.render_template('index.html', has_result=False)
  return flask.render_template_string('look')


@app.route('/classify_stream', methods=['POST'])
def classify_stream():
  global image
  global i
  try:
      data = flask.request.data  # but data will be empty unless the request has the proper content-type header
      if not data:
          data = flask.request.form.keys()[0]
      data = json.loads(data)["json"]
      # data = bytearray(data)
      image[i] = data
      i = i+1
      if(i==512):
        i=0
      cv2.imshow(winName,image)
      return flask.render_template_string('OK')
  except Exception as err:
        traceback.print_exc(file=sys.stdout)
        return flask.render_template_string(str(err))

@app.route('/classify_image', methods=['POST'])
def classify_image():
  global i
  try:
      i=i+1
      data = flask.request.data  # but data will be empty unless the request has the proper content-type header
      if not data:
          data = flask.request.form.keys()[0]
      image = json.loads(data)["json"]
      image=numpy.array(image).astype(numpy.uint8)
      # image=image.transpose()
      cv2.imwrite('RandomGray%d.png'%i,image)
      # cv2.imwrite('RandomGray%d.png'%i, image0, cv2.IMREAD_GRAYSCALE)
      cv2.imshow(winName,image)
      return flask.render_template_string('OK')
  except Exception as err:
        traceback.print_exc(file=sys.stdout)
        return flask.render_template_string(str(err))


# if __name__ == '__main__':
#   # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
#   cv2.imwrite('RandomGray.png', image)
#   cv2.imshow(winName,image )

import threading

class RecordThread(threading.Thread):
         def run(self):
            record()

import json
from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle #json++
import urllib2
import wave
class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct

import httplib
import urllib

def record():
  global i
  global image
  global winName
  FILENAME = 'recording.wav'
  INDEX = 1
  FORMAT = pyaudio.paInt16
  # FORMAT = pyaudio.paInt8
  CHANNELS = 1
  RATE = 48000
  # RATE = 22500
  # INPUT_BLOCK_TIME = 0.05
  INPUT_BLOCK_TIME = 0.1
  INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
  # CHUNK = 512
  # CHUNK = 1024
  # CHUNK = 1024
  # CHUNK = 2048
  CHUNK = 4096
  # CHUNK = 9192
  # len=512
  length=1024
  # length=2048
  # length = 4096
  # step=32
  step=64
  # step=128
  # step=256
  stream = pyaudio.PyAudio().open(
      format = FORMAT,
      channels = CHANNELS,
      rate = RATE,
      input = True,
      frames_per_buffer = CHUNK,
      input_device_index = INDEX )

  # r = numpy.array()
  r = numpy.empty(length)
  offset = 0
  while True:
    try:
      dataraw = stream.read(CHUNK)
      data0 = numpy.fromstring(dataraw, dtype='int16')
      # data0 = numpy.fromstring(dataraw, dtype='int8')
      if(i<20 and numpy.sum(data0)<1000):
        continue

      r=numpy.append(r,data0)

      # Hamming window
#      for(int i = 0; i < SEGMENTATION_LENGTH;i++){ timeDomain[i] = (float) (( 0.53836 - ( 0.46164 * Math.cos( TWOPI * (double)i / (double)( SEGMENTATION_LENGTH - 1 ) ) ) ) * frameBuffer[i]); }

      # print r.size
      while offset < r.size - length :
        data = r[offset:offset+length]
        offset=offset + step
        data = numpy.fft.fft(data)#.abs()
        data = numpy.absolute(data)
        data = data[0:512]/256.0#.split(data,512)
        data = numpy.log2(data*0.05+1.0)#//*50.0;
        numpy.putmask(data, data > 255, 255)

        image[i] = data
        i = i+1
        if(i==512):
          i=0
          # image=image.T
          image=numpy.rot90(image)
          cv2.imshow(winName,image)
          result=upload(image)
          p=re.compile("(\\d)")
          result=p.search(result).group(1)
          # subprocess.call(["say"," %s"%result])
          # os.system("say  %s"%result)
          # subprocess.Popen("say"," %s"%result)

          # cv2.imwrite('RandomGray%d.png'%i,image)
        # if cv2.waitKey(10) == 27: BREAKS portAudio !!
              # cv2.destroyWindow(winName)
              # return 0
    except IOError:
      print 'todo: in threading'
    except  Exception as err:
          print('Upload image error: %s' % err)
          traceback.print_exc(file=sys.stdout)


def upload(image=None):
    if image==None:
      image_file="/me/ai/phonemes/5_Karen_260.wav.spec.png"
    # image_file="/me/ai/phonemes/spoken_numbers/7_Karen_260.wav.spec.png"
      image = skimage.io.imread(image_file).astype(numpy.uint8) #float32 BOTH OK!

    post_data=json.dumps({'json':image.tolist()})
    req = urllib2.Request('http://192.168.1.24:5000/classify_image', post_data)
    response = urllib2.urlopen(req)
    result = response.read()
    print result

if __name__ == '__main__':
  cv2.imshow(winName,image )
  RecordThread().start()
  # record()
  # upload()
  # transform_all()
  # cv2.waitKey()
  # app.run(debug=True, host='0.0.0.0', port=5000)
  # app.run(debug=False, host='0.0.0.0', port=5000)
