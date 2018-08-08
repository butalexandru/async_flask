"""
Flask webserver that counts GPIO hits and shows them on a front page via socketio

24th July 2018
"""

# Start with a basic flask app webpage.
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context, request
from threading import Thread, Event, Timer

__author__ = ''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False

#turn the flask app into a socketio app
socketio = SocketIO(app)

class ScoreBoard():
    def __init__(self):
        self.score = [0, 0]
        self.on = False
        self.pause = False
        self.countdown = 0

    def broadcastData(self):
        socketio.emit('countdown', {'countdown': self.countdown}, namespace='/target')
        socketio.emit('score', {'t0': self.score[0], 't1': self.score[1]}, namespace='/target')
        socketio.emit('state', {'on': self.on, 'pause': self.pause}, namespace='/target')

    def clock(self):
        if self.on and not self.pause and self.countdown != 0 :
            self.countdown = self.countdown-1
            socketio.emit('countdown', {'countdown': self.countdown}, namespace='/target')
        if self.countdown == 0 :
            self.on = False
        #call this function again in one second;
        if self.on:
            Timer(1, self.clock).start()


    def start(self, countdown):
        self.score = [0, 0]
        self.on = True
        self.publish()
        self.countdown = countdown
        self.clock()
        self.broadcastData();

    def stop(self):
        self.on = False
        self.pause = False;
        self.broadcastData();

    def enterPause(self):
        self.pause = True;
        self.broadcastData();

    def resume(self):
        self.pause = False;
        self.broadcastData();

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

@app.route('/view')
def viewScoreSingle():
    return render_template('view.html')

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
    score.start(int(data['countdown']));

@socketio.on('stop', namespace='/target')
def stopScoring(data):
    score.stop();

@socketio.on('pause', namespace='/target')
def pauseScoring(data):
    score.enterPause();

@socketio.on('resume', namespace='/target')
def resumeScoring(data):
    score.resume();

@socketio.on('init', namespace='/target')
def resumeScoring(data):
    score.broadcastData();

#MAIN
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    #socketio.run(app, host='192.168.4.1', port=5000)
