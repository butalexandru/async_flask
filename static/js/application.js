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

var score = 0

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
  //connect to the socket server.
  socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
  $('#countdown-number').html(query.time[0]);
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

function countHits(){
  //receive details from server
  socket.on('newnumber', function(msg) {
    score = score+1;
    $('#score').html(score);
  });
}

function startCountDown() {
  var countdown = query.time[0];
  score = 0;
  $('#score').html(score);

  // show stop / hide start
  startBtnEl.style.display = "none";
  stopBtnEl.style.display = "flex";
  pauseBtnEl.style.display = "flex";

  countHits();

  countdownNumberEl.textContent = countdown;
  //countdownCircleEl.style.animationDuration = countdown+'s';
  //countdownCircleEl.style.animationPlayState = 'running';

  countdownInterval = setInterval(function() {
    if(!isPaused){
      countdown = --countdown;
    }
    if (countdown == 0){
      stopCountDown();
    }
    if (countdown == 1){
      GameOverSound.play();
    }
  
    countdownNumberEl.textContent = countdown;
  }, 1000);
}

function stopCountDown(){
  clearInterval(countdownInterval);
  socket.removeAllListeners('newnumber');

  // show stop / hide start
  startBtnEl.style.display = "flex";
  stopBtnEl.style.display = "none";
  pauseBtnEl.style.display = "none";
  resumeBtnEl.style.display = "none";
}

function pauseCountDown(){
  socket.removeAllListeners('newnumber');
  isPaused = true;
  // show stop / hide start
  pauseBtnEl.style.display = "none";
  resumeBtnEl.style.display = "flex";
}

function resumeCountDown(){
  countHits();
  isPaused = false;

  // show stop / hide start
  pauseBtnEl.style.display = "flex";
  resumeBtnEl.style.display = "none";
}
