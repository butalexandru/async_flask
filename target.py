"""
Flask webserver that counts GPIO hits and shows them on a front page via socketio

24th July 2018
"""

# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request
from threading import Thread, Event

__author__ = 'Alexandru But'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False

#turn the flask app into a socketio app
socketio = SocketIO(app)

class ScoreBoard():
    def __init__(self):
        self.score = [0, 0];
        self.on = False
        self.pause = False

    def start(self):
        self.score = [0, 0];
        self.on = True
        self.publish();

    def stop(self):
        self.on = False;

    def pause(self):
        self.pause = True;

    def resume(self):
        self.pause = False;

    def hit(self, targetId, pinIndex):
        if self.on and not self.pause:
            #here is the place we are checking order of hit
            if self.score[targetId]%5 == pinIndex :
                self.score[targetId] = self.score[targetId]+1
                self.publish()

    def publish(self):
        socketio.emit('score', {'t0': self.score[0], 't1': self.score[1]}, namespace='/target')

score = ScoreBoard();

#HTTP API
@app.route('/')
def index():
    #only by sending self page first will the client be connected to the socketio instance
    return render_template('index.html')

@app.route('/singleplayer')
def singleplayer():
    return render_template('singleplayer.html')

@app.route('/multiplayer')
def multiplayer():
    return render_template('multiplayer.html')

@app.route('/target', methods = ['POST'])
def targetHit():
    targetId = int(request.form.get('targetId'))
    pinIndex = int(request.form.get('pinIndex'))
    score.hit(targetId, pinIndex);
    return('ack');


#Socket API
@socketio.on('connect', namespace='/target')
def target_connect():
    # need visibility of the global thread object
    print('Client connected')

@socketio.on('disconnect', namespace='/target')
def target_disconnect():
    print('Client disconnected')

@socketio.on('start', namespace='/target')
def startScoring(data):
    score.start();

@socketio.on('stop', namespace='/target')
def stopScoring(data):
    score.stop();

@socketio.on('pause', namespace='/target')
def pauseScoring(data):
    score.pause();

@socketio.on('resume', namespace='/target')
def resumeScoring(data):
    score.resume();

#MAIN
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
