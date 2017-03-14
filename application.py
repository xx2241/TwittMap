from flask import *
from twitter_filter import *
application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def start():
    return render_template('TwittMap.html')


@application.route('/keyword', methods=['GET', 'POST'])
def tweetmap():
    if request.method == 'POST':
        print('post')
        tags = request.form['tags']
        print("tags:", tags)
        locs = tweets_filter(tags)
        print("locs:", locs)
        return json.dumps({'locs': locs})
    else:
        return json.dumps({'locs': []})


@application.route('/local', methods=['GET','POST'])
def tweetgeo():
    if request.method == 'GET':
        lat = float(request.args['lat'])
        lng = float(request.args['lng'])
        coordinates = [lng, lat]
        print ([coordinates[1], coordinates[0]])
        locs = tweets_geo(coordinates)
        #locs = {'locs': locs}
        print (locs)
        #return json.dumps({'locs': locs})
        return jsonify({'locs': locs})
    else:
        return jsonify({'locs': []})
        #return json.dumps({'locs': []})


if __name__ == "__main__":
    application.run(debug=True)
