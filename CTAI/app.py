import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from importlib import import_module

import argparse
from urllib import request

import torch
from flask import *

from CTAI_flask.segment_anything import sam_model_registry

import core.main
import core.net.unet as net


UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)

    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/image')
        image_path = os.path.join('./tmp/image', file.filename)
        model_path =r"D:\2024\ssr\BSAM-main\final\CXR_1024multiaug\iter_600.pth"
        image_info=core.main.c_main(image_path,model_path)
        pid = file.filename
        print(image_info["perimeter"][1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/image/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info':image_info
                       })


    return jsonify({'status': 0})

@app.route('/upload2', methods=['GET', 'POST'])
def upload_file2():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)

    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/image')
        image_path = os.path.join('./tmp/image', file.filename)
        model_path=r"D:\2024\ssr\BSAM-main\output\MoNuseg_1024custom_maskatt\iter_600.pth"
        image_info=core.main.c_main(image_path,model_path)
        pid = file.filename
        print(image_info["perimeter"][1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/image/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info':image_info
                       })


    return jsonify({'status': 0})

@app.route('/upload3', methods=['GET', 'POST'])
def upload_file3():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)

    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/image')
        image_path = os.path.join('./tmp/image', file.filename)
        model_path=r"D:\2024\ssr\BSAM-main\final\CHASE_1024multiaug_maskatt2\iter_1000.pth"
        image_info=core.main.c_main(image_path,model_path)
        pid = file.filename
        print(image_info["perimeter"][1])
        return jsonify({'status': 1,
                        'image_url': 'http://127.0.0.1:5003/tmp/image/' + pid,
                        'draw_url': 'http://127.0.0.1:5003/tmp/draw/' + pid,
                        'image_info':image_info
                       })


    return jsonify({'status': 0})

@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)


# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    # print(file)
    if request.method == 'GET':
        if file is None:
            pass
        else:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


def init_model():

    return net


if __name__ == '__main__':
    # with app.app_context():
    #     current_app.model = init_model()
    app.run(host='127.0.0.1', port=5003, debug=True)
