#!/bin/zsh
pushd /home/robert/opt/rabot
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
workon rabot
pip install -r requirements.txt
# debug mode, runs using flask server
#python rabot.py
# production mode, runs using uwsgi server
uwsgi --http-socket 127.0.0.1:5000 --wsgi-file rabot.py --callable app --processes 8 --threads 4 --stats 127.0.0.1:5001
popd
