from flask import Flask
from raweather import RaWeather

app = Flask(__name__)


@app.route("/raweather/check/")
def raweather_check():
    raw = RaWeather()
    jobresults = raw.check()
    return 'ran raweather/check\n{}'.format(jobresults)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
