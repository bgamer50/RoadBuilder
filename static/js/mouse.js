	function setUpMouse() {
        var canvas = document.getElementById("canvas");
		canvas.addEventListener('mousedown', function(evt) {
		rect = canvas.getBoundingClientRect();
			if(new Date().getTime() - window.mouseStartTime > 358) {
				var x = evt.clientX - rect.left;
				var y = evt.clientY - rect.top;
				var gridX = Math.floor(1.0 * x / squareSize);
				var gridY = Math.floor(1.0 * y / squareSize);
				
				if(x < gridWidth && y < gridHeight) {
					/*$.post("/sq", JSON.stringify([gridX, gridY]));
					pause(3);
					$.get("/sq", function(ID) {window.selectedRoadID = parseInt(ID);});
					pause(3);*/
					getSquareInfo(gridX, gridY);
					window.infoBoxTime = new Date().getTime();
					window.infoBoxX = x; window.infoBoxY = y;
				}
				if(x >= 0 && x <= gridWidth - 5 && y >= 0 && y <= gridWidth - 5 && window.mouseFunction == 1) {
				   //Click while creating road
					var lastIndex = window.newRoadPath.length - 1;
					if(lastIndex < 0) {
						window.newRoadPath = [[gridX, gridY]];
						window.pointMatrix = window.pointMatrix.concat([[-1, lastIndex + 1, gridX, gridY]]); //roadID, order, x, y
					}
					//If contiguous
					else if(Math.abs(window.newRoadPath[lastIndex][0] - gridX) <= 1 && Math.abs(window.newRoadPath[lastIndex][1] - gridY) <= 1) {
					    //If it borders only one other point
					    if(borderCount(gridX, gridY) == 1) {
					      window.newRoadPath = window.newRoadPath.concat([[gridX, gridY]]);
					      window.pointMatrix = window.pointMatrix.concat([[-1, lastIndex + 1, gridX, gridY]]); //roadID, order, x, y
					    }			
					}
					//Non-contiguous cases
					else if(gridX - window.newRoadPath[lastIndex][0] > 0 && window.newRoadPath[lastIndex][1] == gridY) { //if the clicked x is greater and y is the same
					    var canBuild = true;
					    /*
					    for(k = window.newRoadPath[lastIndex][0] + 1; k <= gridX; k++) {
					      if(borderCount(k, gridY) > 1) {
						  canBuild = false;
						  break;
						  }
					    } */
					    if(canBuild == true)
					      for(k = window.newRoadPath[lastIndex][0] + 1; k <= gridX; k++) {
						window.newRoadPath = window.newRoadPath.concat([[k, gridY]]);
						window.pointMatrix = window.pointMatrix.concat([[-1, lastIndex + 1, k, gridY]]);
						lastIndex += 1; 
					      }
					}
					else if(gridX - window.newRoadPath[lastIndex][0] < 0 && window.newRoadPath[lastIndex][1] == gridY) { //If the clicked x is less and y is the same
					    for(k = window.newRoadPath[lastIndex][0] - 1; k >= gridX; k--) {
						window.newRoadPath = window.newRoadPath.concat([[k, gridY]]);
						window.pointMatrix = window.pointMatrix.concat([[-1, lastIndex + 1, k, gridY]]);
						lastIndex += 1; 
					    }
					}
					else if(gridY - window.newRoadPath[lastIndex][1] < 0 && window.newRoadPath[lastIndex][0] == gridX) { //If the clicked y is less and x is the same
					    for(k = window.newRoadPath[lastIndex][1] - 1; k >= gridY; k--) {
						window.newRoadPath = window.newRoadPath.concat([[gridX, k]]);
						window.pointMatrix = window.pointMatrix.concat([[-1, lastIndex + 1, gridX, k]]);
						lastIndex += 1; 
					    }
					}
					else if(gridY - window.newRoadPath[lastIndex][1] > 0 && window.newRoadPath[lastIndex][0] == gridX) { //If the clicked y is greater and x is the same
					    for(k = window.newRoadPath[lastIndex][1] + 1; k <= gridY; k++) {
						window.newRoadPath = window.newRoadPath.concat([[gridX, k]]);
						window.pointMatrix = window.pointMatrix.concat([[-1, lastIndex + 1, gridX, k]]);
						lastIndex += 1; 
					    }
					}
					console.log("Grid Clicked at " + gridX + ", " + gridY + "\n");
				}
				else if(x >= 0 && x <= gridWidth - 5 && y >= 0 && y <= gridWidth - 5 && window.definingZone == 1) {
				    window.newZones = window.newZones.concat([[gridX, gridY, document.getElementById("zonebox").value]]);
				    window.zoneMatrix[gridX][gridY] = document.getElementById("zonebox").value;
				}
				var message = 'Mouse position: ' + x + ',' + y;
				window.mouseStartTime = new Date().getTime();
				console.log(message);
			}
		}, false);
	}