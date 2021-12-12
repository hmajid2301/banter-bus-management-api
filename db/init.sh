#!/bin/sh
for filename in /data/management_api/*.json; do
	collectionName=$(basename $filename .json)
	echo "COLLECTION $filename $collectionName"
	mongoimport --collection $collectionName --file $filename --jsonArray -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD -h $MONGO_HOSTNAME -d $MONGO_INITDB_DATABASE --authenticationDatabase admin
done