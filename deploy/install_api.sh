#!/bin/bash
# ---------------------------------------------------------
# Installs esdoc_api onto a webfaction server.
# ---------------------------------------------------------

# Display notice.
printf "*************************************\n"
printf "cim api install :: STARTS\n"
printf "*************************************\n"


# ---------------------------------------------------------
# STEP 0 : Initialize environment.
# ---------------------------------------------------------
printf "*-----------------------------------*\n"
printf "STEP 0 : Initializing environment ...\n"

# Validate params.
if [ $# -ne 5 ]; then
	printf "ERR001 :: Incorrect arguments !"
	echo "Usage:"
	echo " $0 <PLATFORM> <ID> <VERSION> <PORT> <DB_PWD>"
	echo "    PLATFORM => [test | prod ]"
	echo "    ID => integer"
	echo "    VERSION => major.minor.revision (all integers)"
	echo "    PORT => integer"
	echo "    DB_PWD => alpha-numeric with at least one special character"
	exit 1
fi

# Get params.
APP_PLATFORM=$1
APP_ID=$2
APP_VERSION=$3
PORT_NO=$4
DB_PWD=$5

# Set args.
APP_NAME=$APP_PLATFORM"_api"$APP_ID
DB_NAME="esdoc_"$APP_PLATFORM"_api"$APP_ID
DB_USER="esdoc_"$APP_PLATFORM"_api"$APP_ID

# Set directory paths.
HOME=/home/esdoc
WEBAPPS=$HOME/webapps
WEBAPP=$WEBAPPS/$APP_NAME
TEMPLATES=$HOME/templates

# Initialize directory structure.
rm -rf $WEBAPP/app
mkdir $WEBAPP/app
mkdir $WEBAPP/tmp


# ---------------------------------------------------------
# STEP 1 : Installing source.
# ---------------------------------------------------------
printf "*-----------------------------------*\n"
printf "STEP 1 : Installing source ...\n"

# Download source.
git clone https://github.com/ES-DOC/esdoc-api $WEBAPP/tmp

# Remove non-required files.
targets=(
        $WEBAPP"/tmp/src/esdoc_api/config/ini_files"
        $WEBAPP"/tmp/src/esdoc_api/app.wsgi"
        $WEBAPP"/tmp/src/esdoc_api/webrun.py"
)
for target in "${targets[@]}"
do
        rm -rf $target
done

# Copy source.
cp -r -f $WEBAPP/tmp/src/* $WEBAPP/app


# ---------------------------------------------------------
# STEP 2 : Configuring app.
# ---------------------------------------------------------
printf "*-----------------------------------*\n"
printf "STEP 2 : Configuring app ...\n"

# Copy templates.
cp /home/esdoc/templates/api/* /home/esdoc/templates/tmp

# Format templates.
templates=(
        "/home/esdoc/templates/tmp/config.ini"
        "/home/esdoc/templates/tmp/connect.py"
        "/home/esdoc/templates/tmp/db_ingest.py"
        "/home/esdoc/templates/tmp/db_setup.py"
        "/home/esdoc/templates/tmp/httpd.conf"
        "/home/esdoc/templates/tmp/wsgi.py"
)
for template in "${templates[@]}"
do
        perl -e "s/APP_NAME/"$APP_NAME"/g;" -pi $(find $template -type f)
        perl -e "s/APP_VERSION/"$APP_VERSION"/g;" -pi $(find $template -type f)
        perl -e "s/DB_USER/"$DB_USER"/g;" -pi $(find $template -type f)
        perl -e "s/DB_NAME/"$DB_NAME"/g;" -pi $(find $template -type f)
        perl -e "s/DB_PWD/"$DB_PWD"/g;" -pi $(find $template -type f)
        perl -e "s/PORT_NO/"$PORT_NO"/g;" -pi $(find $template -type f)
done

# Transfer templates.
cp /home/esdoc/templates/tmp/config.ini $WEBAPP/app
cp /home/esdoc/templates/tmp/connect.py $WEBAPP/app/esdoc_api/lib/db/pgres
cp /home/esdoc/templates/tmp/db_ingest.py $WEBAPP/app
cp /home/esdoc/templates/tmp/db_setup.py $WEBAPP/app
cp /home/esdoc/templates/tmp/httpd.conf $WEBAPP/apache2/conf
cp /home/esdoc/templates/tmp/wsgi.py $WEBAPP/htdocs


# ---------------------------------------------------------
# STEP 3 : Restore database.
# ---------------------------------------------------------
printf "*-----------------------------------*\n"
printf "STEP 3 : Restoring database ...\n"

unzip $WEBAPP/tmp/deploy/db.zip -d $WEBAPP/tmp/deploy
pg_restore -U $DB_NAME -d $DB_NAME $WEBAPP/tmp/deploy/db

# ---------------------------------------------------------
# STEP 4 : Clear up.
# ---------------------------------------------------------
printf "*-----------------------------------*\n"
printf "STEP 4 : Cleaning up ...\n"
rm -rf /home/esdoc/templates/tmp/*
rm -rf $WEBAPP/tmp

printf "*-----------------------------------*\n"


# Display notice.
printf "*************************************\n"
printf "cim api install :: COMPLETE\n"
printf "*************************************\n"

exit 0
