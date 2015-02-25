	var pointMatrix = []; //road point matrix
	var carMatrix = [];
	var juncMatrix = [];
	var newRoadPath = [];
	var zoneMatrix = [];
	var newZones = [];
	var roads = [];
	var nodes = [];
	var prevCarMatrix = [];
	var squareSize = 12.5;
	var startTime = new Date().getTime();
	var mouseStartTime = startTime;
	var mouseFunction = 0; //0 = default/nothing, 1 = create road
	var gridWidth = 1175;
	var gridHeight = 575;
	var simulationRunning = 1;
	var roadsDrawn = 0;
	var nodesDrawn = 0;
	var junctionsDrawn = 0;
	var zonesDrawn = 0;
	var selectedRoadID = 1;
	var infoBoxX = 0;
	var infoBoxY = 0;
	var infoBoxTime = 0;
	var roadButtonText = "Create Road";
	var editing = 0;
	var definingZone = 0;
	var timeasdf = 0;
	
	function pause(t) { sTime = new Date().getTime(); while(new Date().getTime() - sTime < t); } 
	
	function draw() {
	    
	    var canvas = document.getElementById("canvas");
	    setUpMouse();

        if(canvas.getContext) {
	        var ctx = canvas.getContext("2d");
			
			ctx.fillStyle = "rgb(255,255,255)";
			ctx.fillRect(0, 0, 1175, 575);

	        ctx.fillStyle = "rgba(0,0,200,0.5)";
	        
	        for(x = 0; x < 1175; x += squareSize)
	            for(y = 0; y < 575; y += squareSize)
	                ctx.strokeRect(x, y, squareSize, squareSize);

        drawNodes(ctx);
        drawZones(ctx);
        drawRoadPropertiesDisplay(ctx);
		drawInfoBox(ctx);
	    }
	    
	    if(new Date().getTime() - startTime > 1000) {
			window.startTime = new Date().getTime();
			if(window.simulationRunning == 1)
				drawCars(ctx, 1);
	    }

	    else if(window.simulationRunning == 1) {
	    	drawCars(ctx, 0);
	    }
	    window.setTimeout(draw, 300);

	}

	function drawNodes(ctx) {
		
		getRoads("");
		getNodes("");

		//while(window.nodes.length == 0);

		ctx.fillStyle = "rgb(105, 105, 105)";

		for(var k = 0; k < window.nodes.length; k++) {
			var currentNode = window.nodes[k];
			var x = currentNode[1];
			var y = currentNode[2];
			switch(currentNode[3]) {
				case 0:
					ctx.fillStyle = "rgb(105, 105, 105)";
					break;
				case 1:
					ctx.fillStyle = "rgb(0,255,0)";
					break;
				case 2:
					ctx.fillStyle = "rgb(204,204,0)";
					break;
				case 3:
					ctx.fillStyle = "rgb(0,0,255)";
					break;
			}
			if(currentNode[6] == 1) { //x = lastEntry[1] + 1, y = lastEntry[2] + 1; lastEntry[1] = x - 1, lastEntry[2] = y - 1
				//draw road
				ctx.beginPath();
				ctx.moveTo(squareSize * ((x - 1) + 1), squareSize * (y - 1));
				ctx.lineTo(squareSize * (x + 1), squareSize * y);
				ctx.lineTo(squareSize * ((x - 1) + 1), squareSize * y);
				ctx.lineTo(squareSize * ((x - 1) + 1), squareSize * (y - 1));
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * (x - 1), squareSize * ((y - 1) + 1));
				ctx.lineTo(squareSize * x, squareSize * (y + 1));
				ctx.lineTo(squareSize * x, squareSize * y);
				ctx.lineTo(squareSize * (x - 1), squareSize * ((y - 1) + 1));
				ctx.closePath();
				ctx.fill();

				//draw lines
				
			}
			else if(currentNode[6] == 2) { //x = lastEntry[1] - 1, y = lastEntry[2] - 1
				ctx.beginPath();
				ctx.moveTo(squareSize * ((x + 1) + 1), squareSize * (y + 1));
				ctx.lineTo(squareSize * (x + 1), squareSize * y);
				ctx.lineTo(squareSize * (x + 1), squareSize * (y + 1));
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * (x + 1), squareSize * ((y + 1) + 1));
				ctx.lineTo(squareSize * x, squareSize * (y + 1));
				ctx.lineTo(squareSize * (x + 1), squareSize * (y + 1));
				ctx.closePath();
				ctx.fill();
			}
			else if(currentNode[6] == 3) { //x = lastEntry[1] - 1, y = lastEntry[2] + 1
				ctx.beginPath();
				ctx.moveTo(squareSize * ((x + 1) + 1), squareSize * ((y - 1) + 1));
				ctx.lineTo(squareSize * (x + 1), squareSize * (y + 1));
				ctx.lineTo(squareSize * (x + 1), squareSize * ((y - 1) + 1));
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * (x + 1), squareSize * (y - 1));
				ctx.lineTo(squareSize * x, squareSize * y);
				ctx.lineTo(squareSize * (x + 1), squareSize * ((y - 1) + 1));
				ctx.closePath();
				ctx.fill();
			}
			else if(currentNode[6] == 4) { //x = lastEntry[1] + 1, y = lastEntry[2] - 1
				ctx.beginPath();
				ctx.moveTo(squareSize * x, squareSize * y);
				ctx.lineTo(squareSize * (x - 1), squareSize * (y + 1));
				ctx.lineTo(squareSize * ((x - 1) + 1), squareSize * (y + 1));
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * (x + 1), squareSize * (y + 1));
				ctx.lineTo(squareSize * ((x - 1) + 1), squareSize * ((y + 1) + 1));
				ctx.lineTo(squareSize * ((x - 1) + 1), squareSize * (y + 1));
				ctx.closePath();
				ctx.fill();
			}

	       	ctx.fillRect(squareSize * x, squareSize * y, squareSize, squareSize);
	    }
	}

	function isJunction(loc) {
		for(k = 0; k < juncMatrix.length; k++) {
			if(juncMatrix[k][0] == loc[0] && window.nodes[k][4] == loc[1])
				return 1;
		return 0;
		}
	}
	function drawZones(ctx) {
	  try {
	    for(k = 0; k < newZones.length; k++) {
		 	r = newZones[k][0];
		 	c = newZones[k][1];
		    //residential
		    if(newZones[k][2] == 1)
				ctx.fillStyle = "rgb(0,255,0)";
		    //workplace
		    else if(newZones[k][2] == 2)
				ctx.fillStyle = "rgb(204,204,0)";
		    //commercial/shopping
		    else if(newZones[k][2] == 3)
				ctx.fillStyle = "rgb(0,0,255)";
			//none
		    else
		    	ctx.fillStyle = "rgb(255,255,255)";

		    ctx.fillRect(squareSize * r, squareSize * c, squareSize, squareSize);
		}
	  }
	  catch(err) {;}
	}
	function drawCars(ctx, update) {
		getCars(update);
		ctx.fillStyle = "rgb(0,255,0";
		for(k = 0; k < window.carMatrix.length; k++) {
			x = window.carMatrix[k][0];
			y = window.carMatrix[k][1];
			direction = window.carMatrix[k][2];
			if(direction == 0)
				ctx.fillRect(squareSize * (x + 0.5), squareSize * (y + 0.6), squareSize / 4, squareSize / 4);
			else if(direction == 1)
				ctx.fillRect(squareSize * (x + 0.5), squareSize * (y + 0.2), squareSize / 4, squareSize / 4);
			else if(direction == 2)
				ctx.fillRect(squareSize * (x + 0.7), squareSize * (y + 0.4), squareSize / 4, squareSize / 4);
			else if(direction == 3)
				ctx.fillRect(squareSize * (x + 0.2), squareSize * (y + 0.4), squareSize / 4, squareSize / 4);
		}		
	}
	function drawJunctions(ctx) {
		var x = 0;
		var y = 0;
		for(k = 0; k < window.nodes.length; k++) {
			x = window.nodes[k][1] * squareSize;
			y = window.nodes[k][2] * squareSize;
			//console.log((String)(x) + " " + (String)(y));	
			if(window.nodes[k][4] == 1) {	
				ctx.fillStyle = "rgb(255, 0, 0)";
				ctx.beginPath();
				ctx.arc(x + squareSize / 2.0, y + squareSize / 2.0, squareSize / 2, 0, 2 * Math.PI);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();
			}
			else if(window.nodes[k][4] == 2) {
				ctx.fillStyle = "rgb(0,255,0)";
				ctx.beginPath();
				ctx.arc(x + squareSize / 2.0, y + squareSize / 3.0 - 2, squareSize / 6, 0, 2 * Math.PI);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();

				ctx.fillStyle = "rgb(255,255,0)";
				ctx.beginPath();
				ctx.arc(x + squareSize / 2.0, y + 2 * squareSize / 3.0 - 2, squareSize / 6, 0, 2 * Math.PI);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();

				ctx.fillStyle = "rgb(255,0,0)";
				ctx.beginPath();
				ctx.arc(x + squareSize / 2.0, y + squareSize - 2, squareSize / 6, 0, 2 * Math.PI);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();
			}
			else if(window.nodes[k][4] == 3) {
				ctx.fillStyle = "rgb(255,255,255)";
				ctx.fillRect(x + squareSize / 4.0, y + squareSize / 4.0, squareSize / 2.0, squareSize / 2.0);
				ctx.strokeRect(x + squareSize / 4.0, y + squareSize / 4.0, squareSize / 2.0, squareSize / 2.0);
			}
			else if(window.nodes[k][4] == 6) {
				ctx.fillStyle = "rgb(255, 140, 0)";
				ctx.beginPath();
				ctx.arc(x + squareSize / 2.0, y + squareSize / 2.0, squareSize / 3.0, 0, 2 * Math.PI);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();

				ctx.fillStyle = "rgb(255, 255, 255)";
				ctx.fillRect(x + squareSize / 2.0 - squareSize / 4.0, y + squareSize / 3.0, squareSize / 2.0, squareSize / 4.0);
			}
		}
	}
	function drawInfoBox(ctx) {
		if(selectedRoadID >= 0) {
		  var selectedRoadIndex = -1;
		  for(k = 0; k < roads.length; k++)
			if(parseInt(roads[k][0]) == selectedRoadID) {
				selectedRoadIndex = k;
				break;
			}
		  try {
		  var infoBoxText = roads[selectedRoadIndex][1];
		  }
		  catch(err) {var infoBoxText = "None";}
		}
		else if(selectedRoadID == -1) {
		  var infoBoxText = "Junction";
		}
		else
			var infoBoxText = "None";
		if(new Date().getTime() - infoBoxTime < 3000 && window.simulationRunning != 2) {
			ctx.fillStyle = "rgb(140,140,140)";
			ctx.fillRect(infoBoxX - 2, infoBoxY - 12, 10 * infoBoxText.length, 15);
			ctx.strokeStyle = "rgb(0,0,0)";
			ctx.strokeRect(infoBoxX - 2, infoBoxY - 12, 10 * infoBoxText.length, 15);

			ctx.fillStyle = "rgb(0,100,0)";
			ctx.font = "bold 15px Helvetica";
			ctx.fillText(infoBoxText, window.infoBoxX, window.infoBoxY);
		  }
	}
	function drawRoadPropertiesDisplay(ctx) {
		if(window.selectedRoadID == -1) {
			//then it changes into a junction properties display.
			document.getElementById("namebox").value = "Junction";
			document.getElementById("saveButton").disabled = false; //enable the edit button
		}
		else if(window.selectedRoadID > 0) {	
			var index = -1;
			for(k = 0; k < roads.length; k++)
				if(parseInt(roads[k][0]) == window.selectedRoadID) {
					index = k;
					break;
				}
				if(index >= 0 && window.editing == 0) {
					document.getElementById("namebox").value = String(roads[index][1]);
					document.getElementById("lanesbox").value = String(roads[index][2]);
					document.getElementById("tollbox").value = String(roads[index][3]);
					document.getElementById("speedbox").value = String(roads[index][4]);
					document.getElementById("classbox").value = String(roads[index][5]);
					document.getElementById("saveButton").disabled = false; //enable the edit button
				}
		}
		else {
			window.infoBoxText = "None";
			document.getElementById("namebox").value = "None";
			document.getElementById("lanesbox").value = 0;
			document.getElementById("tollbox").value = 0;
			document.getElementById("speedbox").value = 0;
			document.getElementById("classbox").value = "";
			document.getElementById("saveButton").disabled = true; //disable the edit button
		}
	}
        function drawRoads(ctx) {
	    var lastEntry = new Array();
        for(k = 0; k < pointMatrix.length; k++) {
			var x = pointMatrix[k][2] * squareSize;
	        var y = pointMatrix[k][3] * squareSize;
	             	
			if(pointMatrix[k][0] != -1)
			  ctx.fillStyle = "rgb(105, 105, 105)";
			else
			  ctx.fillStyle = "rgb(130, 105, 105)";
			if(lastEntry[1] + 1 == pointMatrix[k][2] && lastEntry[2] + 1 == pointMatrix[k][3]) { //x + 1, y + 1
				//draw road
				ctx.beginPath();
				ctx.moveTo(squareSize * (lastEntry[1] + 1), squareSize * lastEntry[2])
				ctx.lineTo(squareSize * (pointMatrix[k][2] + 1), squareSize * pointMatrix[k][3])
				ctx.lineTo(squareSize * (lastEntry[1] + 1), squareSize * pointMatrix[k][3])
				ctx.lineTo(squareSize * (lastEntry[1] + 1), squareSize * lastEntry[2])
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * lastEntry[1], squareSize * (lastEntry[2] + 1));
				ctx.lineTo(squareSize * pointMatrix[k][2], squareSize * (pointMatrix[k][3] + 1));
				ctx.lineTo(squareSize * pointMatrix[k][2], squareSize * pointMatrix[k][3]);
				ctx.lineTo(squareSize * lastEntry[1], squareSize * (lastEntry[2] + 1));
				ctx.closePath();
				ctx.fill();

				//draw lines
				
			}
			else if(lastEntry[1] - 1 == pointMatrix[k][2] && lastEntry[2] - 1 == pointMatrix[k][3]) { //x - 1, y - 1
				ctx.beginPath();
				ctx.moveTo(squareSize * (lastEntry[1] + 1), squareSize * lastEntry[2]);
				ctx.lineTo(squareSize * (pointMatrix[k][2] + 1), squareSize * pointMatrix[k][3]);
				ctx.lineTo(squareSize * (pointMatrix[k][2] + 1), squareSize * (pointMatrix[k][3] + 1));
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * lastEntry[1], squareSize * (lastEntry[2] + 1));
				ctx.lineTo(squareSize * pointMatrix[k][2], squareSize * (pointMatrix[k][3] + 1));
				ctx.lineTo(squareSize * lastEntry[1], squareSize * lastEntry[2]);
				ctx.closePath();
				ctx.fill();
			}
			else if(lastEntry[1] - 1 == pointMatrix[k][2] && lastEntry[2] + 1 == pointMatrix[k][3]) { //x - 1, y + 1
				ctx.beginPath();
				ctx.moveTo(squareSize * (lastEntry[1] + 1), squareSize * (lastEntry[2] + 1));
				ctx.lineTo(squareSize * (pointMatrix[k][2] + 1), squareSize * (pointMatrix[k][3] + 1));
				ctx.lineTo(squareSize * lastEntry[1], squareSize * (lastEntry[2] + 1));
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * lastEntry[1], squareSize * lastEntry[2]);
				ctx.lineTo(squareSize * pointMatrix[k][2], squareSize * pointMatrix[k][3]);
				ctx.lineTo(squareSize * lastEntry[1], squareSize * (lastEntry[2] + 1));
				ctx.closePath();
				ctx.fill();
			}
			else if(lastEntry[1] + 1 == pointMatrix[k][2] && lastEntry[2] - 1 == pointMatrix[k][3]) { //x + 1, y - 1
				ctx.beginPath();
				ctx.moveTo(squareSize * pointMatrix[k][2], squareSize * pointMatrix[k][3]);
				ctx.lineTo(squareSize * lastEntry[1], squareSize * lastEntry[2]);
				ctx.lineTo(squareSize * (lastEntry[1] + 1), squareSize * lastEntry[2]);
				ctx.closePath();
				ctx.fill();

				ctx.beginPath();
				ctx.moveTo(squareSize * (pointMatrix[k][2] + 1), squareSize * (pointMatrix[k][3] + 1));
				ctx.lineTo(squareSize * (lastEntry[1] + 1), squareSize * (lastEntry[2] + 1));
				ctx.lineTo(squareSize * (lastEntry[1] + 1), squareSize * lastEntry[2]);
				ctx.closePath();
				ctx.fill();
			}

	        ctx.fillRect(x, y, squareSize, squareSize);
			
			lastEntry[0] = pointMatrix[k][0];
			lastEntry[1] = pointMatrix[k][2];
			lastEntry[2] = pointMatrix[k][3];
        }
	}
	function borderCount(testX, testY) {
	  	var bordering = 0;
		for(k = 0; k < window.newRoadPath.length; k++)
		  if(Math.abs(window.newRoadPath[k][0] - testX) <= 1 && Math.abs(window.newRoadPath[k][1] - testY) <= 1) {
		    bordering += 1;
		  }
		  return bordering;
	}
        window.onload = draw;
