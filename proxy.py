import requests

sessionURL = "https://github.com/session"
token      = "+rK81759IGuJiInpH/xa8R6h0iGEsCZYCGx9VAd78RxyW4xND8Dsec2/XAHZ7WJHm/juaVS4nMrZUssHTBGvXg=="
setCookie  = "_gh_sess=eyJzZXNzaW9uX2lkIjoiMGZlZmMzM2YxZjMzNGIxNGYzMjYyNjFlZWMzNjMyOTYiLCJfY3NyZl90b2tlbiI6IlYzQVU5aWUvSEgwbThLSmR2TDV5bjdIUXloZFVWRmlrS2ptUTFvc1R1a0E9In0%3D--b56dddfb4a83fa4159560bb6e474d410e68a2f1d; path=/; secure; HttpOnly"

req = requests.Request('POST', sessionURL, headers={ 'Cookie': setCookie}, data={'authenticity_token': token, 'login': 'username', 'password': 'secret'}).prepare()

print req.headers

s = requests.Session()
r = s.send(req, verify=False)

print r.headers