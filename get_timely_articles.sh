#!/bin/zsh
pushd /opt/rabot
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv --python=/usr/bin/python3 rabot
workon rabot
pip3 install -r requirements.txt
python /opt/rabot/news.py
popd
