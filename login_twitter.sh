#!/usr/bin/env bash

rm twi.html; rm *.cookies

# curl https://twitter.com/login | grep "authenticity_token" -m 1 | grep -o 'value="[^"]*"' | cut -f 1,7

TOKEN=`curl https://twitter.com/login  --cookie-jar login.cookies | grep "authenticity_token" -m 1 | grep -o 'value="[^"]*"' | cut -c6- | cut -d '"' -f 2`

echo "User: ${USER}, Pass: ${PASS}"

echo "Using token ${TOKEN}"

curl -XPOST https://twitter.com/sessions \
  --cookie login.cookies \
  --cookie-jar session.cookies \
  -H "Content-type: application/x-www-form-urlencoded" \
  --data-urlencode "authenticity_token=${TOKEN}" \
  --data-urlencode "session[username_or_email]=not_lisardo" \
  --data-urlencode "session[password]=**" -v

curl -i https://twitter.com/settings/your_twitter_data --cookie session.cookies > settings.html

