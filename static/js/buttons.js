	function clickCreateRoad() {
	  switch(window.mouseFunction) {
		  case 0:
		    window.mouseFunction = 1;
		    window.simulationRunning = 2; //makes it so that it clicking the start/stop simulation button will not turn the simulation back on.
			document.getElementById("createRoadButton").value = "Finish";
			document.getElementById("defineZoneButton").disabled = true;
			document.getElementById("deleteButton").disabled = true;
			document.getElementById("startSimulationButton").disabled = true;
			document.getElementById("saveButton").disabled = true;
			document.getElementById("namebox").disabled = true;
			document.getElementById("lanesbox").disabled = true;
			document.getElementById("tollbox").disabled = true;
			document.getElementById("speedbox").disabled = true;
			document.getElementById("classbox").disabled = true;
		    break;
		  case 1:
		    window.mouseFunction = 0;
		    window.simulationRunning = 0;
		    if(newRoadPath.length > 0) {
			  input = window.prompt("Name your road:", "Main Street");
			  if(input.length == 0)
			  	input = "Unnamed Road";
			  window.sendNewRoad(input, newRoadPath);
			  window.pause(50);
			  window.pointMatrix = [];
			  window.roadsDrawn = 0; //this is because of road splitting
		    }
		    newRoadPath = [];
			document.getElementById("createRoadButton").value = "Create Road";
			document.getElementById("startSimulationButton").value = "Start Simulation";
			document.getElementById("defineZoneButton").disabled = false;
			document.getElementById("startSimulationButton").disabled = false;
			document.getElementById("deleteButton").disabled = false;
			document.getElementById("saveButton").disabled = false;
			document.getElementById("namebox").disabled = true;
			document.getElementById("lanesbox").disabled = true;
			document.getElementById("tollbox").disabled = true;
			document.getElementById("speedbox").disabled = true;
			document.getElementById("classbox").disabled = true;
			window.roadsDrawn = 0;
			window.junctionsDrawn = 0;
		    break;
	  }
	}
	function clickStartSimulation() {
		switch(simulationRunning) {
			case 1:
				simulationRunning = 0;
				document.getElementById("startSimulationButton").value = "Start Simulation";
				document.getElementById("deleteButton").disabled = false;
				break;
			case 0:
				simulationRunning = 1;
				document.getElementById("startSimulationButton").value = "Stop Simulation";
				document.getElementById("deleteButton").disabled = true;
				break;
		}
	}
	function clickSaveButton() {
		switch(editing) {
			case 0:
				editing = 1;
				document.getElementById("saveButton").value = "Save";
				document.getElementById("defineZoneButton").disabled = true;
				document.getElementById("createRoadButton").disabled = true;
				if(window.selectedRoadID < 0)
					document.getElementById("juncbox").disabled = false;
				else {
					document.getElementById("namebox").disabled = false;
					document.getElementById("lanesbox").disabled = false;
					document.getElementById("tollbox").disabled = false;
					document.getElementById("speedbox").disabled = false;
					document.getElementById("classbox").disabled = false;
				}
				break;
			case 1:
				if(window.selectedRoadID > 0) {
					var newName = document.getElementById("namebox").value;
					var newLanes = document.getElementById("lanesbox").value;
					var newToll = document.getElementById("tollbox").value;
					var newSpeed = document.getElementById("speedbox").value;
					var newClass = document.getElementById("classbox").value;
					if(newName == "")
						window.alert("Invalid name.  Cannot save road.");
					else if(newSpeed == "")
						window.alert("Invalid speed.  Cannot save road.");
					else if(parseInt(newSpeed) > 100)
						window.alert("Speed is above max of 100.  Cannot save road.");
					else if(parseInt(newSpeed) < 10)
						window.alert("Speed is below min of 10.  Cannot save road.");
					else
						updateRoad(selectedRoadID, newName, newLanes, newToll, newSpeed, newClass);
				}
				else {
					var newType = document.getElementById("juncbox").value;
					var newZone = document.getElementById("zonebox").value;
					updateNode(Math.floor(1.0 * window.infoBoxX / squareSize), Math.floor(1.0 * window.infoBoxY / squareSize), newZone, newType);
				}
				editing = 0; 
				document.getElementById("saveButton").value = "Edit";
				document.getElementById("defineZoneButton").disabled = false;
				document.getElementById("createRoadButton").disabled = false;
				document.getElementById("juncbox").disabled = true;
				document.getElementById("namebox").disabled = true;
				document.getElementById("lanesbox").disabled = true;
				document.getElementById("tollbox").disabled = true;
				document.getElementById("speedbox").disabled = true;
				document.getElementById("classbox").disabled = true;
				break;
		}
	}
	function clickDefineZone() {
	  if(window.definingZone == 0) {
	    window.definingZone = 1;
	    window.simulationRunning = 2;
	    document.getElementById("defineZoneButton").value = "Finish";
	    document.getElementById("createRoadButton").disabled = true;
	    document.getElementById("zonebox").disabled = false;
	  }
	  else {
	    window.definingZone = 0;
	    window.simulationRunning = 0;
	    document.getElementById("defineZoneButton").value = "Define Zone";
	    document.getElementById("startSimulationButton").value = "Start Simulation";
	    document.getElementById("createRoadButton").disabled = false;
	    document.getElementById("zonebox").disabled = true;
	    for(k = 0; k < newZones.length; k++)
	    	updateNode(newZones[k][0], newZones[k][1], newZones[k][2], 0);
	    window.newZones = [];	
	  }
	    
	}