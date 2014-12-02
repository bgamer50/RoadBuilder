	var pointMatrix = []; //road point matrix
	var carMatrix = [];
	var juncMatrix = [];
	var newRoadPath = [];
	var zoneMatrix = [];
	var newZones = [];
	var roadInfoMatrix = [];
	var roads = [];
	var nodes = [];
	var prevCarMatrix = null;
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
	
	function getRoadInfo(json) {
		window.roadInfoMatrix = $.parseJSON(json);
	}

	function showAndDrawRoads(json) {
		window.pointMatrix = $.parseJSON(json);
		var ctx = document.getElementById("canvas").getContext("2d");
		drawRoads(ctx);
	}
	function showAndDrawCars(json) {
		window.carMatrix = $.parseJSON(json);
		var ctx = document.getElementById("canvas").getContext("2d");
		drawCars(ctx);
	}
	function showAndDrawJunctions(json) {
		window.juncMatrix = $.parseJSON(json);
		var ctx = document.getElementById("canvas").getContext("2d");
		drawJunctions(ctx);
	}
	function showAndDrawZones(json) {
	    window.zoneMatrix = $.parseJSON(json);
	    var ctx = document.getElementById("canvas").getContext("2d");
	    drawZones(ctx);
	}
	function draw() {
	    
	    var canvas = document.getElementById("canvas");

            if(canvas.getContext) {
                var ctx = canvas.getContext("2d");
		ctx.fillStyle = "rgb(255,255,255)";
		ctx.fillRect(0, 0, 1175, 575);
                //ctx.fillStyle = "rgb(200,0,0)";
                //ctx.fillRect(10, 10, 55, 50);
                ctx.fillStyle = "rgba(0,0,200,0.5)";
                for(x = 0; x < 1175; x += squareSize) {
                    for(y = 0; y < 575; y += squareSize) {
                        ctx.strokeRect(x, y, squareSize, squareSize);
                    }
                }
        drawNodes(ctx);
        drawRoadPropertiesDisplay(ctx);
		drawInfoBox(ctx);
	    }

	    //window.drawn = 0;
	    if(!window.roadsDrawn) {
	    	//$.get("/rds", showAndDrawRoads);
	    	pause(2);
		//$.get("road", getRoadInfo);
		pause(2);
		window.roadsDrawn = 1;
	    }
	    else
		drawRoads(ctx);

	    if(!window.junctionsDrawn) {
	    	//$.get("/junc", showAndDrawJunctions);
	    	pause(2);
	   	 window.junctionsDrawn = 1;
	    }
	    else
		drawJunctions(ctx);
	    
	    if(!window.zonesDrawn) {
		//$.get("/zones", showAndDrawZones);
		pause(2);
		window.zonesDrawn = 1;
	    }
	    else
		drawZones(ctx);
	    
		//Updates car positions.
	    if(new Date().getTime() - startTime > 100) {
		pause(2);
		//$.get("/update", function() {return;});
		pause(2);
		window.startTime = new Date().getTime();
	    }
	    if(window.simulationRunning == 1) {
	    	//$.get("/car", showAndDrawCars);
	    	pause(20);
	    }

	    drawRoadPropertiesDisplay(ctx);
	    drawInfoBox(ctx);
	    
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
			if(juncMatrix[k][0] == loc[0] && juncMatrix[k][1] == loc[1])
				return 1;
		return 0;
		}
	}
	function drawZones(ctx) {
	  try {
	    for(r = 0; r < gridWidth / squareSize; r++)
		for(c = 0; c < gridHeight / squareSize; c++)
		    //residential
		    if(zoneMatrix[r][c] == 1) {
			ctx.fillStyle = "rgb(0,255,0)";
			ctx.fillRect(squareSize * r, squareSize * c, squareSize, squareSize);
		    }
		    //workplace
		    else if(zoneMatrix[r][c] == 2) {
			ctx.fillStyle = "rgb(204,204,0)";
			ctx.fillRect(squareSize * r, squareSize * c, squareSize, squareSize);
		    }
		    //commercial/shopping
		    else if(zoneMatrix[r][c] == 3) {
			ctx.fillStyle = "rgb(0,0,255)";
			ctx.fillRect(squareSize * r, squareSize * c, squareSize, squareSize);
		    }
	  }
	  catch(err) {;}
	}
	function drawCars(ctx) {
		ctx.fillStyle = "rgb(0,200,0)";
		length = 4;
		dxPrime = 0;
		dyPrime = 0;
		var dx = 0;
		var dy = 0;
		for(k = 0; k < carMatrix.length; k++) {
		    dx = carMatrix[k][1][0] - carMatrix[k][0][0];
		    dy = carMatrix[k][1][1] - carMatrix[k][0][1];
		    if(dx == 0 && dy == 0 && prevCarMatrix != null && k < prevCarMatrix.length) {
			dxPrime = dx;
			dyPrime = dy;
			//console.log(prevCarMatrix[k].length)
		    	dx = prevCarMatrix[k][1][0] - prevCarMatrix[k][0][0];
			dy = prevCarMatrix[k][1][1] - prevCarMatrix[k][0][1];
		    }

		    //if(!isJunction(carMatrix[k][0])) {
		    if(0 == 0) {
		    	if(dx == 1 && dy == 1)
				ctx.fillRect(squareSize * carMatrix[k][0][0], squareSize * (carMatrix[k][0][1] + 1), length, length);
		        else if(dx == 1 && dy == -1)
				ctx.fillRect(squareSize * (carMatrix[k][0][0] + 1), squareSize * carMatrix[k][0][1], length, length);
			else if(dx == 1 && dy == 0)
				ctx.fillRect(squareSize * (carMatrix[k][0][0] + 0.5), squareSize * (carMatrix[k][0][1] + 1) - length, length, length);
			else if(dx == 0 && dy == 1)
				ctx.fillRect(squareSize * carMatrix[k][0][0], squareSize * (carMatrix[k][0][1] + 0.5), length, length);
			else if(dx == 0 && dy == -1)
				ctx.fillRect(squareSize * (carMatrix[k][0][0] + 1) - length, squareSize * (carMatrix[k][0][1] + 0.5), length, length);
			else if(dx == -1 && dy == 1)
				ctx.fillRect(squareSize * (carMatrix[k][0][0] - 0.5), squareSize * (carMatrix[k][0][1] + 0.5), length, length);
			else if(dx == -1 && dy == -1)
				ctx.fillRect(squareSize * (carMatrix[k][0][0] + 1) - length, squareSize * carMatrix[k][0][1], length, length);
			else if(dx == -1 && dy == 0)
				ctx.fillRect(squareSize * (carMatrix[k][0][0] + 0.5), squareSize * carMatrix[k][0][1], length, length);
		    }

		    if(dxPrime == 0 && dyPrime == 0 && prevCarMatrix != null && k < prevCarMatrix.length) {
		      try {
		    	carMatrix[k][1][0] = prevCarMatrix[k][1][0];
			carMatrix[k][1][1] = prevCarMatrix[k][1][1];
			carMatrix[k][0][0] = prevCarMatrix[k][0][0];
			carMatrix[k][0][1] = prevCarMatrix[k][0][1];
		      }
		      catch(err) {
			; //do nothing
		      }
		    }
		}
		window.prevCarMatrix = [];
		window.prevCarMatrix = $.extend(true, [], carMatrix);
		
	}
	function drawJunctions(ctx) {
		var x = 0;
		var y = 0;
		for(k = 0; k < juncMatrix.length; k++) {
			x = juncMatrix[k][0][0] * squareSize;
			y = juncMatrix[k][0][1] * squareSize;
			//console.log((String)(x) + " " + (String)(y));	
			if(juncMatrix[k][1] == 1) {	
				ctx.fillStyle = "rgb(255, 0, 0)";
				ctx.beginPath();
				ctx.arc(x + squareSize / 2.0, y + squareSize / 2.0, squareSize / 2, 0, 2 * Math.PI);
				ctx.closePath();
				ctx.fill();
				ctx.stroke();
			}
			else if(juncMatrix[k][1] == 2) {
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
			else if(juncMatrix[k][1] == 3) {
				ctx.fillStyle = "rgb(255,255,255)";
				ctx.fillRect(x + squareSize / 4.0, y + squareSize / 4.0, squareSize / 2.0, squareSize / 2.0);
				ctx.strokeRect(x + squareSize / 4.0, y + squareSize / 4.0, squareSize / 2.0, squareSize / 2.0);
			}
			else if(juncMatrix[k][1] == 6) {
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
		  for(k = 0; k < roadInfoMatrix.length; k++)
			if(parseInt(roadInfoMatrix[k][0]) == selectedRoadID) {
				selectedRoadIndex = k;
				break;
			}
		  try {
		  var infoBoxText = roadInfoMatrix[selectedRoadIndex][1];
		  }
		  catch(err) {var infoBoxText = "None";}
		}
		else if(selectedRoadID < 0) {
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
		if(window.selectedRoadID < 0) {
			//then it changes into a junction properties display.
			document.getElementById("namebox").value = "Junction";
			document.getElementById("lanesbox").disabled = true;
			document.getElementById("tollbox").disabled = true;
			document.getElementById("speedbox").disabled = true;
			document.getElementById("juncbox").disabled = false;
			document.getElementById("classbox").disabled = true;
		}
			
		var index = -1;
		for(k = 0; k < roadInfoMatrix.length; k++)
			if(parseInt(roadInfoMatrix[k][0]) == window.selectedRoadID) {
				index = k;
				break;
			}
			if(index >= 0 && window.editing == 0) {
				document.getElementById("namebox").value = String(roadInfoMatrix[index][1]);
				document.getElementById("lanesbox").value = String(roadInfoMatrix[index][2]);
				document.getElementById("tollbox").value = String(roadInfoMatrix[index][3]);
				document.getElementById("speedbox").value = String(roadInfoMatrix[index][4]);
				document.getElementById("classbox").value = String(roadInfoMatrix[index][5]);
				document.getElementById("lanesbox").disabled = false;
				document.getElementById("tollbox").disabled = false;
				document.getElementById("speedbox").disabled = false;
				document.getElementById("classbox").disabled = false;
				document.getElementById("juncbox").disabled = true;

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

        setUpMouse(); //for some reason this has to be here...	(Found in mouse.js)
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
