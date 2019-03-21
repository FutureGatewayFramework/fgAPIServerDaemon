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
VENV2=venv2
VENV3=venv3
PYTHON2=python2
PYTHON3=python3

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

# $1 - PythonX flag
# $2 - Python venvX file
do_tests() {
  PY_FLAG=$1
  PY_VENV=$2
  echo "Performing tests for $PY_VENV"
  [ $((PY_FLAG)) -eq 0 ] &&\
    echo "Python tests disabled for $PY_VENV" &&\
    return 0
  source $PY_VENV/bin/activate &&\
  pip install -r requirements.txt &&\
  pip install pycodestyle &&\
  check_style &&\
  unit_tests &&\
  deactivate || return 1
}

setup_python() {
  PIP=$(which pip)
  [ "$PIP" = "" ] &&\
    echo "Python pip is not present, unable to perform any test" &&\
    return 1

  PY2_FLAG=$(which $PYTHON2 | wc -l)
  PY2_FAIL=0
  [ $((PY2_FLAG)) -ne 0 ] &&\
    $PYTHON2 -m virtualenv $VENV2 &&\
    echo "Virtual environment for python2 created" ||\
    PY2_FAIL=1

  PY3_FLAG=$(which $PYTHON3 | wc -l)
  PY3_FAIL=0
  [ $((PY3_FLAG)) -ne 0 ] &&\
    $PYTHON3 -m venv $VENV3 &&\
    echo "Virtual environment for python3 created" ||\
    PY3_FAIL=1

  [ $((PY2_FAIL)) -ne 0 ] &&\
    echo "Python2 environment creation failed" &&\
    return 1
  [ $((PY3_FAIL)) -ne 0 ] &&\
    echo "Python3 environment creation failed" &&\
    return 1
  return 0
}

# Releasing
echo "Starting releasing ..." &&\
setup_python &&\
echo "Checking style" &&\
do_tests $PY2_FLAG $VENV2 &&\
do_tests $PY3_FLAG $VENV3 &&\
set_code_headers &&
echo "Done"

