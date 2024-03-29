web: gunicorn wix_tracker.wsgi --log-file -
worker: celery -A wix_tracker worker -l info
celery_beat: celery -A wix_tracker beat