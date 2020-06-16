const express = require('express');
const socket = require('socket.io');
const handlebars = require('express-handlebars');
const fs = require('fs');

// App setup
var app = express();
// Setup handle bars
//instead of app.set('view engine', 'handlebars'); 
app.set('view engine', 'hbs');
//instead of app.engine('handlebars', handlebars({
app.engine('hbs', handlebars({
layoutsDir: __dirname + '/views/layouts',
// set the handle bars file extension.
extname: 'hbs'
}));

// routes
app.get('/', (req, res) => {
//Serves the body of the page aka "main.handlebars" to the container //aka "index.handlebars"
res.render('main', {layout : 'index'});
});

var server = app.listen(3000, function(){
    console.log('listening for requests on port 3000,');
});

// Static files
app.use(express.static('public'));
// Socket setup & pass server
var io = socket(server);
io.on('connection', (socket) => {

    console.log('made socket connection', socket.id);

    // Handle Search event
	socket.on('search', function(data){
		console.log(data.query_str);
		var child = require('child_process').execFile('/usr/bin/python', [
			'/home/ec2-user/simpleApp/search_folder/search.py', data.query_str
		], function(err, stdout, stderr) {
			// Node.js will invoke this callback when process terminates.
                        var out_rawdata = fs.readFileSync('./outfile');
                        var out_data_json = JSON.parse(out_rawdata);
                        console.log(out_data_json)
			socket.emit('search_result', out_data_json);
			//socket.emit('search_result', {'top5':[{message: 'Pittsburgh', title:'Mohammed Sameer'},{message:'Pittsburgh', title:'Phani Teja'}]});
		//	socket.emit('search_result', 
		//		[{message: 'Pittsburgh', title:'Mohammed Sameer'}, 
		//			{message:'Pittsburgh', title:'Phani Teja'}, 
		//			{message: 'Silicon Valley', title:'Cong Zou'}]);
		});
		});
		// console.log(data);

    // Handle typing event
    socket.on('typing', function(data){
        socket.broadcast.emit('typing', data);
    });

});
