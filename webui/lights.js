var lightState = 0;

function initialiseSwitch () {
	
	// Set styling for toggle button
	$( "#lightswitch" ).button();
	
	// Set function to call when toggle button is clicked.
	$( "#lightswitch" ).click(function() {
		toggleLights();
	});		
	
	// Get current light status and configure button appropriately
	var requestURL = "/lightstatus";
	$.ajax({
		url : requestURL,
		type: "GET",				
		success: function(data, textStatus, json) {
			var span = document.getElementById("statusfield");
			var txt = document.createTextNode(data.lightstatus);
			span.innerText = txt.textContent;						
			lightState = data.lightstatus;
			if (lightState == 0) {
				$("#lightswitch").button("option", "label","Switch Lights On");
			} else {
				$("#lightswitch").button("option", "label","Switch Lights Off")
			}			
			$("#lightswitch").button( "enable" );
			},
		error: function (json, textStatus, errorThrown) {
			}	
		});
}			

function toggleLights() {
	if (lightState == 0) {
		$("#lightswitch").button("option", "label","Switch Lights On");
		lightSwitch(1,1);
	} else {
		$("#lightswitch").button("option", "label","Switch Lights Off")		
		lightSwitch(1,0);
	}
}
 
function lightSwitch(lightcode, state) {
	var requestURL = "/lightswitch"; 

    var reqData = {newlightstate: state};						
	$.ajax({
		url : requestURL,
		type: "POST",
		data : reqData,
		success: function(data, textStatus, json) {
			var span = document.getElementById("statusfield");
			var txt = document.createTextNode(data.lightstatus);
			span.innerText = txt.textContent;						
			lightState = data.lightstatus;
			if (lightState == 0) {
				$("#lightswitch").button("option", "label","Switch Lights On");
			} else {
				$("#lightswitch").button("option", "label","Switch Lights Off")
			}
			},
		error: function (json, textStatus, errorThrown) {
			}	
		});
}
