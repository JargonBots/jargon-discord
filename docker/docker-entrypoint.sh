#!/bin/sh

# echo "PWD: $PWD"
# echo `Content: ls -la`

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

exec "$@"