var countdownInterval;
var socket;
//DOM elements
var countdownNumberEl
var countdownCircleEl
var startBtnEl
var stopBtnEl
var pauseBtnEl 
var resumeBtnEl

var isPaused=false;

var GameOverSound = new Audio('static/timeup.wav')
var query

$(document).ready(function(){
  query = param();
  countdownNumberEl = document.getElementById('countdown-number');
  //countdownCircleEl = document.getElementById('circle');
  startBtnEl = document.getElementById('startBtnEl');
  stopBtnEl = document.getElementById('stopBtnEl');
  pauseBtnEl = document.getElementById('pauseBtnEl');
  resumeBtnEl = document.getElementById('resumeBtnEl');
  var targetFeedbackEl = document.getElementById('target_feedback');
  //connect to the socket server.
  socket = io.connect('http://' + document.domain + ':' + location.port + '/target');
  $('#countdown-number').html('-');
  var i;
  var circles = [];
  if (window.location.pathname.includes('view')) {
    // init the target display
    var team = query.team[0];
    $('#team_name').html(team);
    for (i=0; i<5; i++) {
      circles[i] = document.createElement('div');
      circles[i].className = "circle";
      targetFeedbackEl.appendChild(circles[i]);
    }
  } else {
    socket.on('state', function(data) {
      var on = data['on']
      var pause = data['pause']
      if (on) {
        startBtnEl.style.display = "none";
        stopBtnEl.style.display = "";
        pauseBtnEl.style.display = "";
        if (pause) {
          pauseBtnEl.style.display = "none";
          resumeBtnEl.style.display = "";
        } else {
          pauseBtnEl.style.display = "";
          resumeBtnEl.style.display = "none";
        }
      } else {
        startBtnEl.style.display = "";
        stopBtnEl.style.display = "none";
        pauseBtnEl.style.display = "none";
        resumeBtnEl.style.display = "none";
      }
    })
  }
  //receive details from server
  socket.on('score', function(score) {
    if (window.location.pathname.includes('player')) {
      $('#score0').html(score.t0);
      $('#score1').html(score.t1);
    } else {
      var targetIndex = 0;
      if (team == 1) {
        $('#score').html(score.t0);
        targetIndex = score.t0%5;
      } else {
        $('#score').html(score.t1);
        targetIndex = score.t1%5;
      }
      for (i=0; i<5; i++) {
        if (i==targetIndex){
          circles[i].className = "circle hit";
	} else {
          circles[i].className = "circle";
        }
      }
    }
  });

  socket.on('countdown', function(data) {
    countdown = data['countdown'];
    $('#countdown-number').html(countdown);
    if (countdown == 0 && window.location.pathname.includes('player')) {
      stopCountDown();
      GameOverSound.play();
    }
  });

  socket.emit('init', { data: 'data' });
})

function ptq(q)
{
/* parse the query */
/* semicolons are nonstandard but we accept them */
var x = q.replace(/;/g, '&').split('&'), i, name, t;
/* q changes from string version of query to object */
for (q={}, i=0; i<x.length; i++)
  {
  t = x[i].split('=', 2);
  name = unescape(t[0]);
  if (!q[name])
  q[name] = [];
  if (t.length > 1)
    {
    q[name][q[name].length] = unescape(t[1]);
    }
  /* next two lines are nonstandard */
    else
  q[name][q[name].length] = true;
  }
return q;
}

function param() {
  return ptq(location.search.substring(1).replace(/\+/g, ' '));
}

function startCountDown() {
  var countdown = query.time[0];

  socket.emit('start', { 'countdown': countdown});

  // show stop / hide start
  //startBtnEl.style.display = "none";
  //stopBtnEl.style.display = "";
  //pauseBtnEl.style.display = "";
}

function stopCountDown(){
  socket.emit('stop', { data: 'data' });

  // show stop / hide start
  //startBtnEl.style.display = "";
  //stopBtnEl.style.display = "none";
  //pauseBtnEl.style.display = "none";
  //resumeBtnEl.style.display = "none";
}

function pauseCountDown(){
  socket.emit('pause', { data: 'data' });
  isPaused = true;
  // show stop / hide start
  //pauseBtnEl.style.display = "none";
  //resumeBtnEl.style.display = "";
}

function resumeCountDown(){
  socket.emit('resume', { data: 'data' });
  isPaused = false;

  // show stop / hide start
  //pauseBtnEl.style.display = "";
  //resumeBtnEl.style.display = "none";
}
