
#!/bin/bash

cd ~/git/seizure_tracker/seizure_tracker
source seizure/bin/activate
gunicorn application:application -b :8000