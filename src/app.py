from flask import *
from twitter_filter import *
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
	if request.method == 'POST':
		tag = request.form.get('tags')
		print(tag)
		print(tweets_filter(tag))
		return render_template('test2.html',locs=tweets_filter(tag))
	else:
		return render_template('test2.html',locs=[])


if __name__ == "__main__":
	app.run(debug=True)