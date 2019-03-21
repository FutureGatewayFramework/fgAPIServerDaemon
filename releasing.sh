#!/bin/bash
#
# releasing - script that updates releas on python code files
#
# Author: Riccardo Bruno <riccardo.bruno@ct.infn.it>
#

AUTHOR="Riccardo Bruno"
COPYRIGHT=$(date +"%Y")
LICENSE=Apache
VERSION=v0.0.0
MAINTANIER=$AUTHOR
EMAIL=riccardo.bruno@ct.infn.it
STATUS=devel
UPDATE=$(date +"%Y-%m-%d %H:%M:%S")


set_code_headers() {
  TMP=$(mktemp)
  cat >$TMP <<EOF
__author__ = '${AUTHOR}'
__copyright__ = '${COPYRIGHT}'
__license__ = '${LICENSE}'
__version__ = '${VERSION}'
__maintainer__ = '${MAINTANIER}'
__email__ = '${EMAIL}'
__status__ = '${STATUS}'
__update__ = '${UPDATE}'
EOF
  for pyfile in $(/bin/ls -1 *.py *.wsgi tests/*.py); do
      echo "Releasing file: '$pyfile'"
      while read rel_line; do
          rel_item=$(echo $rel_line | awk -F'=' '{ print $1 }' | xargs echo)
          echo "    Processing line item: '$rel_item'"
          CMD=$(echo "sed -i '' s/^${rel_item}.*/\"$rel_line\"/ $pyfile")
          eval $CMD
      done < $TMP
  done
  rm -f $TMP
}

# Call checkstyle
check_style() {
  pycodestyle --ignore=E402 *.py &&\
  pycodestyle tests/*.py
}

# Unittests
unit_tests() {
  TEST_SUITE=(
    fgapiserverdaemon
    fgapiserverdaemon_config
    fgapiserverdaemon_gui
  )
  cd tests
  export PYTHONPATH=$PYTHONPATH:..:.
  export FGTESTS_STOPATFAIL=1
  for test in ${TEST_SUITE[@]}; do
    python -m unittest --failfast test_${test}
    [ $? -ne 0 ] && return 1 
  done
  cd -
}

# Releasing
echo "Starting releasing ..." &&\
check_style &&\
unit_tests &&\
set_code_headers &&
echo "Done"
