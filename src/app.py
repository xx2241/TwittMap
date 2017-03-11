from flask import *
from twitter_filter import *
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
	if request == 'POST':
		tag = request.form.get('tags')
		print(tag)
		return render_template('test.html',locs=tweets_filter('Trump'))
	else:
		return render_template('test.html',locs=[])


if __name__ == "__main__":
	app.run(debug=True)