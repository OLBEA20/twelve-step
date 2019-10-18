#!/bin/sh

set -e

VERSION=$1

echo "{\"tag\":\"${VERSION}\", \"message\": \"Version ${VERSION}\", \"object\": \"${GITHUB_SHA}\", \"type\": \"commit\"}" > tag.json
echo "Creating tag:\n$(cat tag.json)"
curl -s -d @tag.json -H "Authorization: token ${GITHUB_TOKEN}" --header "Content-Type:application/json" "https://api.github.com/repos/OLBEA20/twelve-step/git/tags" --output tag_response.json 
echo "Response:\n$(cat tag_response.json)"

REF_SHA=$(jq '.sha' tag_response.json)
echo "{\"ref\":\"refs/tags/${VERSION}\", \"sha\":${REF_SHA}}" > tag_reference_request.json

echo "Creating reference:\n$(cat tag_reference_request.json)"
curl -s -d @tag_reference_request.json -H "Authorization: token ${GITHUB_TOKEN}" --header "Content-Type:application/json" "https://api.github.com/repos/OLBEA20/twelve-step/git/refs" --output create_reference_response.json 
echo "Response:\n$(cat create_reference_response.json)"
