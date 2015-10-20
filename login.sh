#!/usr/bin/env bash

USER=$1
PASS=$2

rm unseen-repo.html; rm *.cookies

TOKEN=`curl https://github.com/login --cookie-jar login.cookies  | grep "authenticity_token" | grep -o '[^"]*\=\='`

echo "User: ${USER}, Pass: ${PASS}"

echo "Using token ${TOKEN}"

curl -XPOST https://github.com/session \
  --cookie login.cookies \
  --cookie-jar session.cookies \
  -H "Content-type: application/x-www-form-urlencoded" \
  --data-urlencode "utf8=✓" \
  --data-urlencode "authenticity_token=${TOKEN}" \
  --data-urlencode "login=${USER}" \
  --data-urlencode "password=${PASS}" -v

curl -i https://github.com/BearchInc/unseen-core --cookie session.cookies > unseen-repo.html

