import multiprocessing
from flask import Flask, jsonify, send_from_directory, render_template, request
from flask_cors import CORS
import platform
import linux
import windows
import webbrowser
import consts
import os
import pickle
import sys
from pathlib import Path
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def self_dir():
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    return base_path


app = Flask(__name__,
            template_folder=os.path.join(self_dir(), 'html'))
cors = CORS(app)

cred = {}
try:
    with open(os.path.join(self_dir(), 'credentials'), 'rb') as file:
        old = pickle.load(file)
        cred = {'url': old['url'],
                'username': old['username'],
                'password': old['password']}
except FileNotFoundError:
    cred = {'url': '', 'username': '', 'password': ''}


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(self_dir(), 'html', 'js'), path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(os.path.join(self_dir(), 'html', 'css'), path)


@app.route('/')
def root():
    return render_template("index.html")


@app.route('/step')
def status():
    if platform.system() == 'Linux':
        return jsonify(linux.step)
    elif platform.system() == 'Windows':
        return jsonify(windows.step)
    else:
        return ''


@app.route('/credentials')
def credentials():
    global cred
    try:
        with open(os.path.join(self_dir(), 'credentials'), 'rb') as file:
            old = pickle.load(file)
            cred = {'url': request.args['url'] or old['url'],
                    'username': request.args['username'] or old['username'],
                    'password': request.args['password'] or old['password']}
    except FileNotFoundError:
        cred = {'url': '', 'username': '', 'password': ''}
    with open(os.path.join(self_dir(), 'credentials'), 'wb') as file:
        pickle.dump(cred, file)
    return jsonify(cred)


@app.route('/backup')
def backup():
    global cred
    if platform.system() == 'Linux':
        linux.backup(cred['url'], cred['username'], cred['password'])
    elif platform.system() == 'Windows':
        windows.backup(cred['url'], cred['username'], cred['password'])
    else:
        OSError('Not compatible with operating system')
    return ''


@app.route('/restore')
def restore():
    global cred
    if platform.system() == 'Linux':
        linux.restore(cred['url'], cred['username'], cred['password'])
    elif platform.system() == 'Windows':
        windows.restore(cred['url'], cred['username'], cred['password'])
    else:
        OSError('Not compatible with operating system')
    return ''


def flask():
    app.run()


if __name__ == "__main__":
    p = multiprocessing.Process(target=flask)
    p.start()
    if not consts.dev:
        webbrowser.open('http://127.0.0.1:5000', new=2)
