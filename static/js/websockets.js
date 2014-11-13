function getRoads(message) {
	if ("WebSocket" in window) {
    	var ws = new WebSocket("ws://localhost:8888/r?Id=123456789");
    	ws.onopen = function() {
        	ws.send(message);
    	};
    	ws.onmessage = function (evt) { 
    	    var received_msg = evt.data;
    	    console.log(received_msg);
    	    window.roads = $.parseJSON(received_msg);
    	};
    	ws.onclose = function() { 
        	return;
    	};
	} else {
    	console.log("Error: WebSockets not supported by browser");
    	return;
	}
}

function getNodes(message) {
	if ("WebSocket" in window) {
    	var ws = new WebSocket("ws://localhost:8888/n?Id=123456789");
    	ws.onopen = function() {
        	ws.send(message);
    	};
    	ws.onmessage = function (evt) { 
    	    var received_msg = evt.data;
    	    console.log(received_msg);
    	    window.nodes = $.parseJSON(received_msg);
    	};
    	ws.onclose = function() { 
        	return;
    	};
	} else {
    	console.log("Error: WebSockets not supported by browser");
    	return;
	}
}


function pause(t) { sTime = new Date().getTime(); while(new Date().getTime() - sTime < t); }