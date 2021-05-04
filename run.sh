#!/bin/bash

source seizure/bin/activate
gunicorn application:application -b :8000