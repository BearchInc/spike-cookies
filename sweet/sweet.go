package sweet

import (
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"strings"
)

type Request struct {
	client   *SweetClient
	req      *http.Request
	endpoint string
	payload  string
}

type SweetClient struct {
	*http.Client
}

func NewWithClient(client *http.Client) *SweetClient {
	return &SweetClient{client}
}

func (client *SweetClient) EnableCookieJar() *SweetClient {
	jar, _ := cookiejar.New(nil)
	client.Client.Jar = jar
	return client
}

func (client *SweetClient) PostForm(endpoint string, payload url.Values) *Request {
	body := payload.Encode()
	req, err := http.NewRequest("POST", endpoint, strings.NewReader(body))
	if err != nil {
		return nil
	}

	req.Header.Add("Content-Length", "156") // strconv.Itoa(len(body)))
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded; param=value")

	return &Request{
		req:      req,
		client:   client,
		endpoint: endpoint,
		payload:  body,
	}
}

func (req *Request) AddCookie(cookie *http.Cookie) *Request {
	req.req.AddCookie(cookie)
	return req
}

func (req *Request) SetHeader(key, val string) *Request {
	req.req.Header.Set(key, val)
	return req
}

func (req *Request) SetHeaderValues(key string, vals []string) *Request {
	req.req.Header[key] = vals
	return req
}

func (request *Request) Do() (*http.Response, error) {
	resp, err := request.client.Do(request.req)
	return resp, err
}