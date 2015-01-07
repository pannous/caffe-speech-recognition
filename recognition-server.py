#!/usr/bin/env python
import os
import sys
import time
import logging
import flask
import werkzeug
import optparse
import tornado.wsgi
import tornado.httpserver
import numpy as np
import pandas as pd
from PIL import Image
from flask.ext.cors import CORS
import cStringIO as StringIO
import urllib
import skimage.io
import json
import traceback
# from skimage.color import rgb2gray

import caffe

REPO_DIRNAME = os.path.abspath(os.path.dirname(__file__) + '/..')
UPLOAD_FOLDER = '/tmp/caffe_demos_uploads'

# Obtain the flask app object
app = flask.Flask(__name__)
#  allow other sites to post data to this service by our Ajax
cors = CORS(app)


@app.route('/')
def index():
    return flask.render_template_string("please use recognition-server with record.py") #  template('index.html', has_result=False)


@app.route('/record', methods=['GET'])
def record():
    return flask.render_template('Recorder.html', has_result=False)


@app.route('/RecorderJS/<path:image_file>')
def static_proxy(image_file):
    # send_static_file will guess the correct MIME type
    return flask.send_from_directory('/me/caffe/python/templates/RecorderJS/', image_file)
#     return app.send_static_file(os.path.join('/me/caffe/python/templates/RecorderJS/', path))



i = 0
buff = np.ndarray(shape=(512, 512), dtype=np.uint8)


@app.route('/classify_stream', methods=['POST'])
def classify_stream():
    global i
    try:
        data = flask.request.data  # but data will be empty unless the request has the proper content-type header
        if not data:
            data = flask.request.form.keys()[0]
        data = json.loads(data)["json"]
        # data = bytearray(data)
        buff[i] = data
        i = i+1
        if i == 512:
            i = 0
            print "Classification ... "
            image = buff[:, :, np.newaxis] / 255.
            result = app.clf.classify_image(image)
            return result[2]
        return '...'
    except Exception as err:
        logging.info('Upload image error: %s', err)
        traceback.print_exc(file=sys.stdout)
        return 'Upload image error: %s' % err


nr = 0


@app.route('/classify_image', methods=['POST'])
def classify_image():
    global nr
    nr = nr + 1
    try:
        data = flask.request.data  # but data will be empty unless the request has the proper content-type header
        if not data:
            data = flask.request.form.keys()[0]
            #            print data
        #            data = urllib.decode(data)
        jdata = json.loads(data)
        data = jdata["json"]
        clazz = 'unknown'  # jdata["class"]  # learn if different from prediction
        net_name = 'speech'
        if "class" in jdata:
            clazz = jdata["class"]
        if "net" in jdata:
            net_name = jdata["net"]
        # data = bytearray(data)
        print len(data)
        image = np.asarray(data).astype(np.uint8)  # egal? (np.float32)  # (np.uint8) for imsave !
        print "-------------------------"
        print image.shape
        if not clazz == 'unknown':
            skimage.io.imsave("/data/saved/classify_%s_%s.%d.png" % (net_name, clazz, nr), image)
        image = image[:, :, np.newaxis]
        result = app.clf.classify_image(image)
        if result[0]:
            print "YAY, got result %s" % result[2]
            return flask.render_template_string(str(result[2]))
        else:
            return flask.render_template_string("NONE")
    except Exception as err:
        logging.info('Upload image error: %s', err)
        traceback.print_exc(file=sys.stdout)
        return 'Upload image error: %s' % err


class SpeechClassifier(object):
    default_args = {
        'model_def_file': ('model.pbxtext'),
        'pretrained_model_file': ('weights.caffemodel'),
        'mean_file': (None),
        'class_labels_file': (None),
    }

    default_args['image_dim'] = 256
    default_args['raw_scale'] = 255.
    default_args['swap_colors_wtf'] = False
    default_args['gpu_mode'] = True

    def __init__(self, model_def_file, pretrained_model_file, mean_file,
                 raw_scale, class_labels_file, image_dim, gpu_mode, swap_colors_wtf):
        logging.info('Loading net and associated files...')
        if swap_colors_wtf:
            print("swap_colors_wtf")
            swap = (2, 1, 0)
        else:
            print("OK, not swapping any colors")
            swap = False
        model = "numbers_deploy.prototxt"
        weights = "numbers_iter_5000.caffemodel"
#        model = "words_deploy.prototxt"
#        weights = "words_iter_1000.caffemodel"
        print "model_def %s" % model
        print "model_file %s" % weights
        print "image_dims=(%d,%d)" % (int(image_dim), int(image_dim))
        print "raw_scale=%d" % int(raw_scale)
        print "mean=%s" % mean_file
        print "channel_swap=%s" % str(swap)
        print "gpu_mode %s" % gpu_mode

        # better do caffe.Classifier(...).predict by hand:
        self.net = caffe.Net(model, weights)
#        help(self.net)
        self.net.set_phase_test()
        self.net.set_raw_scale('data', 255.0)
        self.net.set_mode_gpu()

        if class_labels_file:
            with open(class_labels_file) as f:
                labels_df = pd.DataFrame([
                    {
                        'synset_id': l.strip().split(' ')[0],
                        'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
                    }
                    for l in f.readlines()
                ])
                self.labels = labels_df.sort('synset_id')['name'].values

    def classify_image(self, image):
        starttime = time.time()
        data = np.asarray([self.net.preprocess('data', image)])
        out = self.net.forward_all(data=data)
        print "classification %s" % out['words0s'].flatten()
#        print "classification class: %d" % out['prob'][0].argmax(axis=0)
#        print "probability %d" % out['prob'][0].max(axis=0)
        endtime = time.time()
        meta = out['words0s'][0].max(axis=0)
#        bet_result = out['words0s'][0].argmax(axis=0)
        bet_result = out['words0s'].flatten()
        return (True, meta, bet_result, '%.3f' % (endtime - starttime))


def start_tornado(app, port=5000):
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    print("Tornado server starting on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()


def start_from_terminal(app):
    """
    Parse command line options and start the server.
    """
    parser = optparse.OptionParser()
    parser.add_option(
        '-d', '--debug',
        help="enable debug mode",
        action="store_true", default=False)
    parser.add_option(
        '-p', '--port',
        help="which port to serve content on",
        type='int', default=5000)
    parser.add_option(
        '-g', '--gpu',
        help="use gpu mode",
        action='store_true', default=True)
    parser.add_option(
        '-m', '--model',
        help="proto definition of net to use (prototxt)")
    parser.add_option(
        '-w', '--weights',
        help="trained net to use (caffemodel|prototxt)")
    parser.add_option(
        '-x', '--image_dim',
        default=512,
        help="image dimension height==width")
    parser.add_option(
        '-l', '--labels',
        help="labels file")
    parser.add_option(
        '-s', '--dont_swap_colors_wtf',
        action='store_true',
        help="Normal color mapping"
    )
    parser.add_option(
        '-0', '--grey',
        action='store_true',
        help="The net expects gray images")

    opts, args = parser.parse_args()
    default_args = SpeechClassifier.default_args
    default_args.update({'gpu_mode': opts.gpu})
    if opts.model:
        default_args.update({'model_def_file': opts.model})
    if opts.weights:
        default_args.update({'pretrained_model_file': opts.weights})
    if opts.labels:
        default_args.update({'class_labels_file': opts.labels})
    # default_args.update({'image_dim': opts.image_dim})
    # print "opts.dont_swap_colors_wtf %s" % str(opts.dont_swap_colors_wtf)
    # default_args.update({'swap_colors_wtf': not opts.dont_swap_colors_wtf})

    # Initialize classifier
    app.clf = SpeechClassifier(**SpeechClassifier.default_args)

    if opts.debug:
        app.run(debug=True, host='0.0.0.0', port=opts.port)
    else:
        start_tornado(app, opts.port)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    start_from_terminal(app)
