document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.3.32";   // the IP address of your Raspberry PI

function client(){
    
    const net = require('net');
    var input = document.getElementById("message").value;
    console.log("THIS WAS RUN TOO")

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function send_data(data) {
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${data}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// update data for every 50ms
function update_data(){
    setInterval(function(){
        // get image from python server
        client();
    }, 50);
}

document.addEventListener('DOMContentLoaded', function() {
    // const client = client();
    // document.getElementById("")
    const net = require('net');

    let client;

    function connectToServer(port, host) {
    // Establish connection to the server

    client = net.createConnection({ port, host }, () => {
        console.log(`Connected to server at ${host}:${port}`);
    });

    // Handle incoming data from the server
    client.on('data', (data) => {
        console.log('Received from server:', data.toString());
    });

    // Handle client disconnection
    client.on('end', () => {
        console.log('Disconnected from server');
    });
    }

    // Function to send data to the server
    function sendData(data) {
        console.log(client)
    if (client && client.writable) {
        client.write(data, (err) => {
        if (err) {
            console.error('Error sending data:', err);
        } else {
            console.log(`Sent to server: ${data}`);
        }
        });
    } else {
        console.error('Client is not connected or writable');
    }
    }

    // Example Usage
    connectToServer(server_port, server_addr);

    // Example of sending data to the server
    setTimeout(() => {
    sendData('Hello, server!');
    }, 1000);

    setTimeout(() => {
    sendData('Here is some more data.');
    }, 2000);

})