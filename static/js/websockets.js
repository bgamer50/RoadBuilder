function getRoads(message) {
	if ("WebSocket" in window) {
    	var ws = new WebSocket("ws://localhost:8888/r?Id=123456789");
    	ws.onopen = function() {
        	ws.send(message);
    	};
    	ws.onmessage = function (evt) { 
    	    var received_msg = evt.data;
    	    //console.log(received_msg);
    	    window.roads = $.parseJSON(received_msg);
    	    ws.close();
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
    	    //console.log(received_msg);
    	    window.nodes = $.parseJSON(received_msg);
    	    ws.close();
    	};
    	ws.onclose = function() { 
        	return;
    	};
	} else {
    	console.log("Error: WebSockets not supported by browser");
    	return;
	}
}

function sendNewRoad(roadName, path) {
	if("WebSocket" in window) {
		var ws = new WebSocket("ws://localhost:8888/s?Id=12345678");
		ws.onopen = function() {
			tempArray = [roadName, path];
			ws.send(JSON.stringify(tempArray));
		};
		ws.onmessage = function(evt) {
			var received_msg = evt.data;
			console.log(received_msg);
		};
		ws.onclose = function() {
			return;
		};
	} else {
		console.log("Error: Websockets not supported by browser");
		return;
	}
}

function getSquareInfo(x, y) {
	if("WebSocket" in window) {
		var ws = new WebSocket("ws://localhost:8888/sq?Id=12345678");
		ws.onopen = function() {
			tempArray = [x, y];
			ws.send(JSON.stringify(tempArray));
		};
		ws.onmessage = function(evt) {
			var received_msg = evt.data;
			window.selectedRoadID = parseInt(received_msg);
			ws.close();
		};
		ws.onclose = function() {
			return;
		};
	} else {
		console.log("Error: Websockets not supported by browser");
		return;
	}	
}

function updateRoad(id, name, lanes, toll, speed, classification) {
	if("WebSocket" in window) {
		var ws = new WebSocket("ws://localhost:8888/ur?Id=12345678");
		ws.onopen = function() {
			tempArray = [id, name, lanes, toll, speed, classification];
			ws.send(JSON.stringify(tempArray));
			ws.close();
			getRoads("none");
		};
		ws.onclose = function() {
			return
		};
	}
	else {
		console.log("Error:Websockets not supported by browser");
		return;
	}
}

function updateNode(x, y, zone, juncType) {
	if("WebSocket" in window) {
		var ws = new WebSocket("ws://localhost:8888/un?Id=12345678");
		ws.onopen = function() {
			tempArray = [x, y, zone, juncType];
			ws.send(JSON.stringify(tempArray));
			ws.close();
			getNodes("none");
		};
		ws.onclose = function() {
			return
		};
	}
	else {
		console.log("Error:Websockets not supported by browser");
		return;
	}
}

function getCars(update) {
	if("WebSocket" in window) {
		var ws = new WebSocket("ws://localhost:8888/car?Id=12345678");
		ws.onopen = function() {
			ws.send(JSON.stringify(update));
		};
		ws.onmessage = function(evt) {
			var received_msg = evt.data;
			window.roadMatrix = $.parseJSON(received_msg);
			ws.close();
		};
		ws.onclose = function() {
			return
		};
	}
	else {
		console.log("Error:Websockets not supported by browser");
		return;
	}

}

function pause(t) { sTime = new Date().getTime(); while(new Date().getTime() - sTime < t); }