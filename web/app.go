package web

import (
	"github.com/PuerkitoBio/goquery"
	"github.com/drborges/demo-app/sweet"
	"github.com/julienschmidt/httprouter"
	"net/http"
	"net/url"
	"google.golang.org/appengine"
	"google.golang.org/appengine/urlfetch"
)

var (
	LoginURL   = "https://github.com/login"
	SessionURL = "https://github.com/session"
)

func init() {
	router := httprouter.New()

	router.POST("/login", func(w http.ResponseWriter, req *http.Request, params httprouter.Params) {
		cxt := appengine.NewContext(req)
		urlfetchClient := urlfetch.Client(cxt)
		client := sweet.NewWithClient(urlfetchClient).EnableCookieJar()
		resp, _ := client.Get(LoginURL)

		doc, _ := goquery.NewDocumentFromReader(resp.Body)
		sel := doc.Find("input[name=authenticity_token]")
		token, _ := sel.Attr("value")

		form := url.Values{}
		form.Add("login", "user")
		form.Add("password", "secret")
		form.Add("authenticity_token", token)

		resp, _ = client.PostForm(SessionURL, form).Do()
		for _, cookie := range resp.Cookies() {
			w.Header().Add("Cookie", cookie.String())
		}
	})

	http.Handle("/", router)
}
