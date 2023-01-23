var app = require('express')();
var express = require('express');
var path = require('path');
var http = require('http').Server(app);
const io = require('socket.io')(http);
const Kafka = require('kafka-node');
const Consumer = Kafka.Consumer;
const client = new Kafka.KafkaClient({ kafkaHost: 'localhost:9092' });

const topics = [{
  topic: 'test',
}];
const options = {
  autoCommit: true,
  fetchMaxWaitMs: 1000,
  fetchMaxBytes: 1024 * 1024,
  encoding: 'buffer',
};
app.use(express.static(path.join(__dirname, "imgs")));
app.get("/", function(req, res){
    res.sendFile(__dirname + '/default.html');
})
const consumer = new Consumer(client, topics, options);
consumer.on('message', (message) => {
  //console.log('message:', message);
  const buf = Buffer.from(message.value, 'binary');
  const data = JSON.parse(buf.toString());
  io.emit('linechart', data);
 // console.log(data);
});
consumer.on('error', (err) => {
  console.log('Error:', err);
});
http.listen(5000, function(){
    console.log("server running on, 5000");
})

