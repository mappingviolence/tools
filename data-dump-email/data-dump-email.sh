#!/bin/sh
text="This is the data dump for $(date +%F)"
subject="Mapping Violence Data Dump for $(date +%B)"
email_file=data-dump-email/emails.txt
body_path="/tmp/usr/script/mailx"
body_file="$body_path""/body_file.txt"
docker_container="mappingviolence_production-mongodb.mappingviolence_1"
docker_script_path="/usr/src/scripts"
docker_script_file="$docker_script_path""/data-extraction.js"
json_file="$docker_script_path""/data.json"

if [ ! -d "$body_path" ]; then
    mkdir -p "$body_path";
fi

echo "$text" > $body_file

docker exec -it "$docker_container" sh -c "mkdir -p /usr/src/scripts && touch $json_file"
docker cp data-dump-email/data-extraction.js "$docker_container":"$docker_script_file"
docker exec -it "$docker_container" sh -c "mongo --quiet $docker_script_file > $json_file"
docker cp "$docker_container":$json_file data-dump-email/data.json

mailx -s "$subject" -a data-dump-email/data.json $(awk '{ line = $1 " " line }; END { print line; }' $email_file) < $body_file
