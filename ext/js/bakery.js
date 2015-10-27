window.bakery = window.bakery || {};

window.bakery.create = function(provider) {
	var container = document.createElement('div'),
		button = document.createElement('button'),
		label = document.createTextNode(provider.label);

	button.className += 'btn'

	button.appendChild(label);
	container.appendChild(button);
	document.body.appendChild(container);

	button.onclick = function() {
		var request = new XMLHttpRequest();
		console.log('Will request authorization');
		request.onreadystatechange = function() {
			if (request.readyState == 4 && request.status == 200) {
				console.log('Request succeed');
			}
		}

		request.open("GET", provider.session, true);
		request.send(null);
	}
};

(function() {
	var providers = {
		github: {
			label: "GitHub",
			session: "http://localhost:8080/login/github"
		},
		facebook: {
			label: "Facebook",
			session: "http://localhost:8080/login/facebook"
		},
		twitter: {
			label: "Twitter",
			session: "http://localhost:8080/login/twitter"
		}
	}

	for (name in providers) {
		window.bakery.create(providers[name]);
	}
})();
