from flask import Flask
from raweather import RaWeather
from ragatherer import RaGatherer


app = Flask(__name__)


@app.route("/raweather/check/")
def raweather_check():
    raw = RaWeather()
    job_results = raw.check()
    app.logger.info(job_results)
    return 'ran raweather/check\n{}'.format(job_results)


@app.route("/ragatherer/check/")
def ragatherer_check():
    rag = RaGatherer("http://feeds.reuters.com/Reuters/worldNews")
    job_results = rag.check()
    app.logger.info(job_results)
    return 'ran ragatherer/check\n{}'.format(job_results)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
