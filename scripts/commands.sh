#!/bin/sh

set -e

wait_psql.sh
migrate.sh
init_setup.sh
runserver.sh