#!/usr/bin/env bash

grep ^Total $1| gawk --csv '{print $11}'

