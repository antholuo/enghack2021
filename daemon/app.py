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
from pathlib import Path

app = Flask(__name__,
            template_folder=os.path.join(Path(__file__).parents[1], 'website', 'dist'))
cors = CORS(app)

cred = {}
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials'), 'rb') as file:
    try:
        old = pickle.load(file)
        cred = {'url': old['url'],
                'username': old['username'],
                'password': old['password']}
    except FileNotFoundError:
        cred = {'url': '', 'username': '', 'password': ''}


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(Path(__file__).parents[1], 'website', 'dist', 'js'), path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(os.path.join(Path(__file__).parents[1], 'website', 'dist', 'css'), path)


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
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials'), 'rb') as file:
        try:
            old = pickle.load(file)
            cred = {'url': request.args['url'] or old['url'],
                    'username': request.args['username'] or old['username'],
                    'password': request.args['password'] or old['password']}
        except FileNotFoundError:
            cred = {'url': '', 'username': '', 'password': ''}
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials'), 'wb') as file:
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
