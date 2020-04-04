#! /bin/bash

usage() {
  echo "Usage $0 [-p|-u] [-f FILE]"
}

if [ $# -lt 1 ]
then
  usage
  exit 0
fi

TIMESTAMP=`date +%F`
BACKUP_FILE="parts-db-$TIMESTAMP.tar.gz"

PACK=0
UNPACK=0
FILE_IN=0
while getopts "hpuf:" opt; do
  case "$opt" in
  h)
    usage
    exit 0
    ;;
  p)  PACK=1
      ;;
  u)  UNPACK=1
      ;;
  f)  BACKUP_FILE=$OPTARG
      FILE_IN=1
      ;;
  esac
done

if [ $PACK -eq 1 ]
then
  # compress
  # Make tmp dir and cp instance files
  mkdir tmp
  cp instance/parts.sqlite tmp/.
  cp -r partridge/data tmp/.

  # tar it up
  tar cvzf $BACKUP_FILE tmp
  
  # rm tmp dir
  rm -r tmp

  echo "Backup complete: $BACKUP_FILE"
else
  # extract
  if [ $FILE_IN -eq 0 ]
  then
    echo "Error: file must be specified when un-packing"
      exit 1
  fi
  if [ ! -f "$BACKUP_FILE" ]
  then
    echo "Error: file not found"
    exit 2
  fi

  # untar
  tar xf $BACKUP_FILE

  # unpack contents of tmp dir
  if [[ ! -d tmp || ! -d tmp/data  || ! -e tmp/parts.sqlite ]]
  then
    echo "Error: Unknown backup file format"
    exit 3
  fi
  mkdir -p instance
  cp -vi tmp/parts.sqlite instance/.
  mkdir -p partridge/data
  cp -v tmp/data/* partridge/data/.

  # rm tmp dir
  rm -r tmp

  echo "Un-pack operation complete"
fi

