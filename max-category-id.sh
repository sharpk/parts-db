#! /bin/sh

cut --delimiter=\" -f 4 partridge/static/class.xml | sort -n | tail -1

