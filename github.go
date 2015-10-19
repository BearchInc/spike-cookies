package main

import (
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"golang.org/x/crypto/ssh/terminal"
	"golang.org/x/net/html"
	"log"
	"net/http"
	"net/url"
	"strconv"
	"strings"
)

var (
	loginFormURL = "https://github.com/login"
	sessionURL   = "https://github.com/session"
)

func ExtractToken(attributes []html.Attribute) string {
	var token string
	found := false
	for _, attr := range attributes {
		if attr.Key == "name" && attr.Val == "authenticity_token" {
			found = true
		}

		if attr.Key == "value" {
			token = attr.Val
		}
	}

	if found {
		return token
	}

	return ""
}

func main() {
	var username string
	fmt.Println("Username:")
	fmt.Scanln(&username)

	fmt.Println("Password:")
	bytePassword, err := terminal.ReadPassword(0)
	if err != nil {
		log.Fatal(err)
	}

	log.Println("> Login to Github as", username)

	http.HandleFunc("/login", func(w http.ResponseWriter, req *http.Request) {
		loadLoginPageResponse, err := http.Get(loginFormURL)
		if err != nil {
			log.Fatal(err)
		}
		defer loadLoginPageResponse.Body.Close()

		doc, err := goquery.NewDocumentFromReader(loadLoginPageResponse.Body)
		if err != nil {
			log.Fatal(err)
		}

		var authenticityToken string
		for _, input := range doc.Find("#login form div input").Nodes {
			if authenticityToken = ExtractToken(input.Attr); authenticityToken != "" {
				break
			}
		}

		fmt.Println("> authenticity_token=" + authenticityToken)

		body := url.Values{}
		body.Add("utf8", "✓")
		body.Add("authenticity_token", authenticityToken)
		body.Add("login", username)
		body.Add("password", string(bytePassword))

		encodedBody := body.Encode()

		loginReq, err := http.NewRequest("POST", sessionURL, strings.NewReader(encodedBody))
		if err != nil {
			log.Fatal(err)
		}

		cookies := loadLoginPageResponse.Header["Set-Cookie"]
		fmt.Println("Cookies: %+v", cookies)

		loginReq.Header.Set("User-Agent", "curl/7.43.0")
		loginReq.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		loginReq.Header.Set("Content-Length", strconv.Itoa(len(encodedBody)))
		loginReq.Header.Add("Cookie", cookies[0])
		loginReq.Header.Add("Cookie", cookies[1])

		sessionResponse, err := http.DefaultClient.Do(loginReq)
		if err != nil {
			log.Fatal(err)
		}

		log.Println("/session body:", encodedBody)
		log.Println("/session response code:", sessionResponse.Status)
	})

	http.ListenAndServe(":8080", nil)
}
