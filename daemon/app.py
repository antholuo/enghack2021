import io

from flask import Flask, jsonify, blueprints, request, redirect, url_for
from flask_cors import CORS
import platform
import linux
import windows
import webbrowser
import consts
import os
import pickle

app = Flask(__name__)
cors = CORS(app)

cred = {}
with open(f'{os.path.dirname(os.path.realpath(__file__))}/credentials', 'rb') as file:
    try:
        old = pickle.load(file)
        cred = {'url': old['url'],
                'username': old['username'],
                'password': old['password']}
    except FileNotFoundError:
        cred = {'url': '', 'username': '', 'password': ''}


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
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/credentials', 'rb') as file:
        try:
            old = pickle.load(file)
            cred = {'url': request.args['url'] or old['url'],
                    'username': request.args['username'] or old['username'],
                    'password': request.args['password'] or old['password']}
        except FileNotFoundError:
            cred = {'url': '', 'username': '', 'password': ''}
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/credentials', 'wb') as file:
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


if __name__ == "__main__":
    app.run(debug=True)
    if not consts.dev:
        webbrowser.open('http://127.0.0.1:5000', new=2)
