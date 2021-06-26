from flask import Flask, render_template, Response, request, redirect, url_for
from daemon import linux, windows
import platform

app = Flask(__name__)

@app.route('/')

@app.route('/backup', methods=['GET'])
def backup( ):
    if platform.system() == 'Linux':
        return linux.backup()
    elif platform.system() == 'Windows':
        return windows.backup()
    else:
        return OSError('Not compatibile with operating system')

@app.route('/restore')
def restore():
    if platform.system() == 'Linux':
        return linux.restore()
    elif platform.system() == 'Windows':
        return OSError('Not compatibile with operating system')
    else:
        return 

if __name__ == "__main__":
    app.run(debug=True)