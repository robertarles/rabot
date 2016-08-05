from flask import Flask
from flask import render_template
from flask import make_response
from raweather import RaWeather
from ragatherer import RaGatherer
from curator import Curator
from cartographer import Cartographer
import ralocation

app = Flask(__name__)
curator = Curator()
cort = Cartographer()


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


@app.route("/curator/recent/")
def curator_recent():
    response_text = ''
    doc_list = curator.get_recent_vault_activity(limit=20)
    for doc in doc_list:
        response_text += '{}:{}</br>'.format(doc['message'], doc['date_updated'])
    return '{}'.format(response_text)


@app.route("/ralocation/update/")
def ralocation_update():
    ralocation.update_location()
    return 'ralocation updated'


@app.route("/cartographer/")
def cartographer():
    coords = cort.get_ra_iphone_coords()
    print(type(cartographer))
    response = make_response(
        render_template(
            'ralocation.html',
            latitude=coords[0],
            longitude=coords[1],
            maps_api_key=cort.get_maps_api_key())
    )
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
