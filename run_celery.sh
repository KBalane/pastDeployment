#!/bin/bash

NAME="digiinsurance"                                # Name of the application
DJANGODIR=/home/django/DigiInsurance-backend/       # Django project directory
USER=django                                         # the user to run as
GROUP=django                                        # the group to run as
CONCURRENCY=5                                       # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=digiinsurance.settings       # which settings file should Django use
DJANGO_WSGI_MODULE=digiinsurance.wsgi               # WSGI module name

echo "Starting $NAME Celery as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
# source /home/ubuntu/apps/.apptitude_envs
# source /home/ubuntu/.venvs/apptitude/bin/activate
source /home/django/.virtualenvs/digiinsurance-env/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

exec celery -A digiinsurance worker -l info --concurrency=${CONCURRENCY}
