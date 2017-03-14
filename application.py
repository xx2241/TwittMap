from flask import *
from twitter_filter import *
application = Flask(__name__)


#@application.route('/', methods=['GET','POST'])
#def init():
#    return render_template('TwittMap.html')


@application.route('/', methods=['GET','POST'])
def tweetmap():
    if request.method == 'POST':
        tag = request.form.get('tags')
        return render_template('TwittMap.html', locs=tweets_filter(tag))
    else:
        return render_template('TwittMap.html', locs=[])


@application.route('/local', methods=['GET','POST'])
def tweetgeo():
    if request.method == 'POST':
        lat = float(request.args['lat'])
        lon = float(request.args['lon'])
        coordinates = [lat, lon]
        return render_template('TwittMap.html', locs=tweets_geo(coordinates))
    else:
        return render_template('TwittMap.html', locs=[])


if __name__ == "__main__":
    application.run(debug=True)
