from flask import *
from twitter_filter import *
application = Flask(__name__)

@application.route('/', methods=['GET','POST'])
def tweetmap():
	if request.method == 'POST':
		tag = request.form.get('tags')
		print(tag)
		print(tweets_filter(tag))
		return render_template('TwittMap.html', locs=tweets_filter(tag))
	else:
		return render_template('TwittMap.html', locs=[])


if __name__ == "__main__":
	application.run(debug=True)
