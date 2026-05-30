#!/usr/bin/env bash
cat $1 | gawk --csv '{print $2}'
