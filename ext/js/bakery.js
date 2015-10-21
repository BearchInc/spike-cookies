window.bakery = window.bakery || {};

window.bakery.github = {
	login: function () {
		console.log('login to github');
	}
};

(function() {
	var loginBtn = document.getElementById("github-login");
	var resultDiv = document.getElementById("result");

	loginBtn.onclick = function() {
		var xmlHttp = new XMLHttpRequest();
		xmlHttp.onreadystatechange = function() {
			if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
				console.log("#####")
				result.innerHTML = xmlHttp.responseText;
			}
		}
		xmlHttp.open("GET", "http://www.github.com", true);
		xmlHttp.send(null);
	}
})();