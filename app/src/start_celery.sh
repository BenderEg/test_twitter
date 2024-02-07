#!/bin/sh
celery -A config worker -B --loglevel="$CELERY_LOG_LEVEL"