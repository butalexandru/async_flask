function multiplayer() {
  window.location.href = '/multiplayer?time=' + document.getElementById("time_s").value;
}

function singleplayer() {
  window.location.href = '/singleplayer?time=' + document.getElementById("time_s").value;
}
