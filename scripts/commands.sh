#!/bin/sh

set -e

wait_psql.sh
migrate.sh
runserver.sh