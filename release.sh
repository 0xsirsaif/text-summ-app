#!/bin/sh

set -e

# shellcheck disable=SC1083
IMAGE_ID=$(docker inspect "${HEROKU_REGISTRY_IMAGE}" --format={{.Id}})
echo IMAGE_ID

PAYLOAD='{"updates": [{"type": "web", "docker_image": "'"$IMAGE_ID"'"}]}'
echo PAYLOAD

curl -n -X PATCH https://api.heroku.com/apps/"$HEROKU_APP_NAME"/formation \
  -d "${PAYLOAD}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
  -H "Authorization: Bearer ${HEROKU_AUTH_SECRET}"