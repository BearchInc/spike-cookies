package providers

import (
	"github.com/PuerkitoBio/goquery"
	"github.com/drborges/demo-app/bakery"
	"github.com/drborges/demo-app/sweet"
	"net/http"
	"net/url"
)

const (
	GithubLoginURL   = "https://github.com/login"
	GithubSessionURL = "https://github.com/session"
)

type GithubProvider struct {
	client *sweet.Client
}

func NewGithubProvider(client *http.Client) *GithubProvider {
	return &GithubProvider{sweet.NewWithClient(client).EnableCookieJar()}
}

func (github *GithubProvider) Login() (bakery.Session, error) {
	resp, err := github.client.Get(GithubLoginURL)
	if err != nil {
		return nil, err
	}

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, err
	}

	sel := doc.Find("input[name=authenticity_token]")
	token, err := sel.Attr("value")
	if err != nil {
		return nil, err
	}

	form := url.Values{}
	form.Add("login", "user")
	form.Add("password", "secret")
	form.Add("authenticity_token", token)

	resp, err = github.client.PostForm(GithubSessionURL, form).Do()
	if err != nil {
		return nil, err
	}

	session := bakery.Session{}
	for _, cookie := range resp.Cookies() {
		session[cookie.Name] = cookie.Value
	}

	return session, nil
}
