from flask import *
from twitter_filter import *
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def tweetmap():
	lat = request.args['lat']
	lon = request.args['lon']
	print(lat)
	print(lon)
    if request.method == 'POST':
        tag = request.form.get('tags')
        print(tag)
        print(tweets_filter(tag))
        return render_template('TwittMap.html', locs=tweets_geo([40.8, -73.9]))
    else:
        return render_template('TwittMap.html', locs=[])
'''
@app.route('/local', methods=['GET','POST'])
def getlocal():
	#if request.method == 'POST':
		lat = request.args['lat']
		lon = request.args['lon']
		print(lat)
		print(lon)
		return render_template('TwittMap.html',locs=[])
'''


if __name__ == "__main__":
    app.run(debug=True)
