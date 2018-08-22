// socket
const socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
  send();
});
socket.on('pong_from_server', function() {
  const latency = new Date - last;
  $('#latency').text(latency + 'ms');
  if (time)
    time.append(new Date, latency);
  setTimeout(send, 100);
});
socket.on('disconnect', function() {
  if (smoothie)
    smoothie.stop();
  $('#transport').text('(disconnected)');
});

const last;
function send() {
  last = new Date;
  socket.emit('ping_from_client');
  $('#transport').text(socket.io.engine.transport.name);
}
