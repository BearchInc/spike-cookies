chrome.runtime.onStartup.addListener(function() {
	chrome.storage.local.get("registered", function(result) {
		console.log(result["registered"]);
		console.log(JSON.stringify(result));

		if (result["registered"])
			return;

		console.log("Registering for push");
		var senderIds = ["752048825109"];
		chrome.gcm.register(senderIds, registerCallback);
	});
});

function registerCallback(registrationId) {
	if (chrome.runtime.lastError) {
		console.log("Registration failed:" + chrome.runtime.lastError);
		// When the registration fails, handle the error and retry the registration later.
		return;
	}

	console.log("Registration id: " + registrationId);
	console.log("Sending registration id.");

	sendRegistrationId(function(succeed) {
		console.log("Sending registration id callback: " + succeed);
		// Once the registration token is received by your server,
		// set the flag such that register will not be invoked
		// next time when the app starts up.
		if (succeed)
			chrome.storage.local.set({
				registered: true,
				gcm: registrationId
			});
	});
}

function sendRegistrationId(callback) {
	// Send the registration token to your application server in a secure way.
	callback(true)
}

function hasStoredCookies(cookiesStored) {
	for (key in cookiesStored) {
		if (cookiesStored[key] == false) {
			return false;
		}
	}
	return true;
}

chrome.gcm.onMessage.addListener(function(message) {
	console.log("Notification received.");
	console.log(message);

	var sessionInfo = message["data"]["cookies"];	
	var providerHome = message["data"]["provider_home"];
	var providerDomain = message["data"]["provider_domain"];

	console.log(sessionInfo);

	var cookies = JSON.parse(sessionInfo);
	var cookiesStored = {};
	for (key in cookies) {
		cookiesStored[key] = false;
	}	

	for (key in cookies) {
		console.log(key + " - " + cookies[key]);
		chrome.cookies.set({
			url: providerHome,
			domain: providerDomain,
			name: key,
			value: cookies[key]
		}, function() {
			cookiesStored[key] = true
			if (hasStoredCookies(cookiesStored)) {
				chrome.tabs.create({
					url: providerHome
				}, function() {
					console.log("redirecting to", providerHome);
				});
			}
			console.log('cookies set, result:', this);
		});
	}
});

// goog.appengine.DevSocket.BASE_URL = "http://localhost:8080/_ah/channel/";


var request = new XMLHttpRequest();
console.log('Will request authorization');
request.onreadystatechange = function() {
	if (request.readyState == 4 && request.status == 200) {
		console.log('Request succeed');
		console.log(request);
		console.log(request.responseText.replace('"', '').replace('"', ''));

		var channel = new goog.appengine.Channel(request.responseText.replace('"', '').replace('"', ''));
		var socket = channel.open(handler);
		// socket.onopen = onOpened;
		// socket.onmessage = onMessage;
		// socket.onerror = onError;
		// socket.onclose = onClose;
	}
}

request.open("GET", "https://bakery-dot-staging-api-getunseen.appspot.com/munjal", true);
request.send(null);

var handler = {
    onopen: function () { alert("onopen") },
    onerror: function (m, u, j) { 
    	console.log(m);
    	console.log(u);
    	console.log(j);
    	alert("onerror") 
    },
    onclose: function () { alert("onclose") },
    onmessage: function (evt) {
        //evt.data will be what the server sends in channel.send_message
        console.log("evt.data received from authhandler: " + evt.data);
        alert("evt.data is: " + evt.data)
    }
};

// function onOpened() {
//     console.log('onOpened');
//     var connected = true;
// }
// function onMessage(msg_obj) {
//     console.log('onMessage');
// }
// function onError(obj) {
//     console.log('onError');
// }
// function onClose(obj) {
//     console.log('onClose');
// }





