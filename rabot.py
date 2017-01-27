from flask import Flask
from flask import render_template
from flask import make_response
from flask import request
from flask import jsonify
from meteorologist import Meteorologist
from ragatherer import RaGatherer
from curator import Curator
from cartographer import Cartographer
from news import Reporter

app = Flask(__name__)
curator = Curator()
cort = Cartographer()
johnny_onthespot = Reporter()


@app.route("/news/post_timely_articles/")
def post_timely_articles():
    hot_trends_list = johnny_onthespot.get_hot_trends()
    johnny_onthespot.post_articles(hot_trends_list)
    return 'ran news/post_timely_articles/\n{}'.format(hot_trends_list)

@app.route("/news/submit_timely_article/", methods=['POST'])
def submit_timely_artcle():
    response = {}
    if request.form["secret_key"] == "fandango":
        if request.form["submit_url"]:
            response = johnny_onthespot.post_submission(request.form["submit_url"])
        else:
            response = {"sucess": False, "error": "Did you send a 'submit_url'?"}
    else:
        response = {"success": False, "error": "Bad secret_key, homer. Try again?"}
    return jsonify(response)



@app.route("/meteorologist/check/")
def meteorologist_check():
    sunny = Meteorologist()
    job_results = sunny.check()
    app.logger.info(job_results)
    return 'ran meteorologist/check\n{}'.format(job_results)


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


@app.route("/cartographer/location/update/")
@app.route("/cartographer/location/update/<name>")
def ralocation_update(name=""):
    cort = Cartographer()
    cort.update_location()
    return 'ran cartographer/update'


@app.route("/cartographer/")
@app.route("/cartographer/location/")
@app.route("/cartographer/location/<name>")
def cartographer_location(name=""):
    ''' where am we? '''
    coords = cort.get_ra_iphone_coords()
    response = make_response(
        render_template(
            'cartographer.html',
            latitude=coords[0],
            longitude=coords[1],
            maps_api_key=cort.get_maps_api_key())
    )
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
