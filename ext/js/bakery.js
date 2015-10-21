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
		request.onreadystatechange = function() {
			if (request.readyState == 4 && request.status == 200) {
				var sessionInfo = JSON.parse(request.responseText);
				for (key in sessionInfo.cookies) {
					chrome.cookies.set({url: provider.home,  domain: provider.domain, name: key, value: sessionInfo.cookies[key]}, function() {
						console.log('cookies set, result:', this)
					});
				}

				chrome.tabs.create({url: provider.home}, function () {
					console.log("redirecting to", provider.home)
				});
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
			home: "https://github.com",
			domain: ".github.com",
			session: "https://bakery-dot-staging-api-getunseen.appspot.com/login/github"
		},
		facebook: {
			label: "Facebook",
			home: "https://facebook.com",
			domain: ".facebook.com",
			session: "https://bakery-dot-staging-api-getunseen.appspot.com/login/facebook"
		},
		twitter: {
			label: "Twitter",
			home: "https://twitter.com",
			domain: ".twitter.com",
			session: "https://bakery-dot-staging-api-getunseen.appspot.com/login/twitter"
		}
	}

	for (name in providers) {
		window.bakery.create(providers[name]);
	}
})();
