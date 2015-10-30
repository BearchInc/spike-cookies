CONFIRMATION_TOKEN=`curl -i https://twitter.com/settings/account --cookie session.cookies --cookie-jar settings.cookies | grep "authenticity_token" -m 1 | grep -o 'value="[^"]*"' | cut -c6- | cut -d '"' -f 2`

curl -XPOST https://twitter.com/settings/your_twitter_data/verify_password \
  --cookie settings.cookies \
  --cookie-jar confirmed.cookies \
  -H "Content-type: application/x-www-form-urlencoded; charset=UTF-8" \
  -H "referer: https://twitter.com/settings/account" \
  --data-urlencode "authenticity_token=${CONFIRMATION_TOKEN}" \
  --data-urlencode "password=**" -v

sleep 1
curl -i https://twitter.com/settings/your_twitter_data --cookie confirmed.cookies > confirmed.html
