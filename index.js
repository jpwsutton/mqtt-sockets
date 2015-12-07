var fs = require('fs');
var mqtt    = require('mqtt');
var path  = require('path');


var configurationFile = 'config.json';

console.log('mqtt-sockets starting.');

var configuration = JSON.parse(fs.readFileSync(configurationFile));

var topicMap = {};

// First we want to get our MQTT Connection ready
var opts = {};
if('server' in configuration.mqttConfig){
  opts.host = configuration.mqttConfig.server;
}
if('port' in configuration.mqttConfig){
  opts.port = configuration.mqttConfig.port;
}
if('username' in configuration.mqttConfig){
  opts.username = configuration.mqttConfig.username;
}
if('password' in configuration.mqttConfig){
  opts.password = configuration.mqttConfig.password;
}
if('clientId' in configuration.mqttConfig){
  opts.clientId = configuration.mqttConfig.clientId;
}
if('ca' in configuration.mqttConfig){
  opts.ca = [];
  // Assume all certs are in this directory.
  for( var cert in configuration.mqttConfig.ca){
    opts.ca.push(
      fs.readFileSync(
        path.join(__dirname, configuration.mqttConfig.ca[cert])
      )
    );
  }
  opts.rejectUnauthorized = false;
}


var client  = mqtt.connect(opts);

console.log('Connect issued');

client.on('connect', function () {
  console.log('Connected!');

   for(var socket in configuration.sockets){
     console.log('Subscribing to: ' +configuration.sockets[socket].topic);
     client.subscribe(configuration.sockets[socket].topic);
     topicMap[configuration.sockets[socket].topic] = configuration.sockets[socket];
   }
});

client.on('message', function (topic, message) {
  // Get the socket that this is for
  var socket = topicMap[topic];
  console.log('Message Arrived for socket: ' + socket.name + ' : ' + message.toString());
  var msg = JSON.parse(message.toString);


  if(socket.type === 'RAW'){
    if(msg.state === 1){
      // Turn on command
      //socket.OnCommand;
    } else {
      // Turn off command
      // socket.OffCommand;
    }
  } else if ( socket.type === 'B'){
    if(msg.state === 1){
      // Turn on
    } else {
      // Turn off
    }
  }



});
