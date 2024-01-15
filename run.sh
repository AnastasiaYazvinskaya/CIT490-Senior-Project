#!/usr/bin/env bash
# exit on error
set -o errexit

cd resultfit

gunicorn resultfit.wsgi