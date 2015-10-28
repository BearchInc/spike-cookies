from google.appengine.api import app_identity
import os
import socket

def current_ip():
	hostname = app_identity.app_identity.get_default_version_hostname()
	ips = { "localhost:8080": "http://" + local_ip() + ":8080",
			"staging-api-getunseen.appspot.com": "https://bakery-dot-staging-api-getunseen.appspot.com" }
	return ips[hostname]


def local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	ip = s.getsockname()[0]
	s.close()
	return ip

