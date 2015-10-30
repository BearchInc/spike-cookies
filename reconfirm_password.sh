TOKEN=`curl -i https://twitter.com/settings/account --cookie session.cookies | grep "authenticity_token" -m 1 | grep -o 'value="[^"]*"' | cut -c6- | cut -d '"' -f 2`

curl -XPOST https://twitter.com/settings/your_twitter_data/verify_password \
  --cookie session.cookies \
  --cookie-jar confirmed.cookies \
  -H "Content-type: application/x-www-form-urlencoded" \
  --data-urlencode "authenticity_token=${TOKEN}" \
  --data-urlencode "password=**" -v

curl -i https://twitter.com/settings/your_twitter_data --cookie confirmed.cookies > settings.html
