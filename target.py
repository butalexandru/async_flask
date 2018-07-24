"""
Flask webserver that counts GPIO hits and shows them on a front page via socketio

24th July 2018
"""

# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from threading import Thread, Event

from targetInterface import TargetInterface

__author__ = 'Alexandru But'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False

#turn the flask app into a socketio app
socketio = SocketIO(app)

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@app.route('/singleplayer')
def singleplayer():
    return render_template('singleplayer.html')

@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

@socketio.on('connect', namespace='/target')
def target_connect():
    # need visibility of the global thread object
    print('Client connected')


@socketio.on('disconnect', namespace='/target')
def target_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    print('1')
    target = TargetInterface(socketio.emit('hit_1', {'hits': 1}, namespace='/target'), socketio.emit('hit_2', {'hits': 1}, namespace='/target'))
    socketio.run(app, host='192.168.4.1')
