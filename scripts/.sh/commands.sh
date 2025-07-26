#!/bin/sh

set -e

/scripts/.sh/wait_psql.sh
/scripts/.sh/migrate.sh
/scripts/.sh/runserver.sh