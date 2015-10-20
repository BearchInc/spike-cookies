package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"github.com/drborges/demo-app/go/sweet"
	"net/url"
)

var (
	LoginURL   = "https://github.com/login"
	SessionURL = "https://github.com/session"
)

func main() {
	client := sweet.NewWithCookieJar()
	resp, _ := client.Get(LoginURL)

	doc, _ := goquery.NewDocumentFromReader(resp.Body)
	sel := doc.Find("input[name=authenticity_token]")
	token, _ := sel.Attr("value")

	form := url.Values{}
	form.Add("login", "username")
	form.Add("password", "secret")
	form.Add("authenticity_token", token)

	resp, _ = client.PostForm(SessionURL, form).Do()

	for _, cookie := range resp.Cookies() {
		fmt.Printf("%v=%v\n", cookie.Name, cookie.Value)
	}
}
