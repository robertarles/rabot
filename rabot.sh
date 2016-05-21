uwsgi --http-socket 127.0.0.1:5000 --wsgi-file rabot.py --callable app --processes 8 --threads 4 --stats 127.0.0.1:5001
