#!/bin/sh
text="Hi team,

Attached you will find the export of the current data in the database. This is the data dump for $(date +%F). Please let me know if you have any questions. Reminder that this export of data includes the POIs that are still in the Draft Stage. \


Best,"
subject="Mapping Violence Data Export for $(date +%B)"
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

echo -n "Please enter your Brown email: "
read -e sender_email

echo "$text" > $body_file

docker exec -it "$docker_container" sh -c "mkdir -p /usr/src/scripts && touch $json_file"
docker cp data-dump-email/data-extraction.js "$docker_container":"$docker_script_file"
docker exec -it "$docker_container" sh -c "mongo --quiet $docker_script_file > $json_file"
docker cp "$docker_container":$json_file data-dump-email/data.json

mailx -s "$subject" -r "$sender_email" -a data-dump-email/data.json $(awk '{ line = $1 " " line }; END { print line; }' $email_file) < $body_file
