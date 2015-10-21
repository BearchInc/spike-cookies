package web

import (
	"github.com/drborges/demo-app/bakery/providers"
	"github.com/julienschmidt/httprouter"
	"google.golang.org/appengine"
	"google.golang.org/appengine/urlfetch"
	"gopkg.in/unrolled/render.v1"
	"net/http"
)

func init() {
	type JSON map[string]interface{}
	router := httprouter.New()
	send := render.New()

	router.POST("/login", func(w http.ResponseWriter, req *http.Request, params httprouter.Params) {
		cxt := appengine.NewContext(req)
		client := urlfetch.Client(cxt)

		session, err := providers.NewGithubProvider(client).Login()
		if err != nil {
			send.JSON(w, http.StatusBadRequest, JSON{"message": err})
			return
		}

		send.JSON(w, http.StatusOK, session)
	})

	http.Handle("/", router)
}
