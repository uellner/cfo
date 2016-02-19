#!/usr/bin/env bash
# Setup file for vagrant

#############
# Constants #
#############

PROJECT_NAME=cfo

export DB_NAME=cfo
export DB_USER=vagrant
export DB_PASS=vagrant

PROJECT_DIR=/home/vagrant/$PROJECT_NAME
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

#########################
# Postgres Installation #
#########################

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list';
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -

sudo apt-get update -y;
sudo apt-get install -y postgresql postgresql-contrib libpq-dev;

##########################
# Postgres Configuration #
##########################

sudo -u postgres createdb $DB_NAME;
echo "CREATE ROLE $DB_USER WITH LOGIN PASSWORD '$DB_PASS'; "| sudo -u postgres psql;
echo "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER; " | sudo -u postgres psql;
echo "ALTER USER $DB_USER CREATEDB;" | sudo -u postgres psql;

###########################
# Virtualenv Installation #
###########################

sudo apt-get install -y python3-pip python3-dev;
sudo pip3 install virtualenv virtualenvwrapper;

#######################
# Pillow Requirements #
#######################

sudo apt-get install -y libtiff4-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev;

##################################
# Virtualenv Setup Configuration #
##################################

echo 'export WORKON_HOME=$HOME/.virtualenvs' >> /home/vagrant/.profile;
echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.4' >> /home/vagrant/.profile;
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/vagrant/.profile;

source /home/vagrant/.profile;
cd $HOME/$PROJECT_NAME;
mkvirtualenv --python=/usr/bin/python3.4 $PROJECT_NAME -r requirements.txt -a .;

###################
# Database Settings #
###################

./manage.py migrate;
