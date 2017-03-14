from flask import *
from twitter_filter import *
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def tweetmap():
    if request.method == 'POST':
        tag = request.form.get('tags')
        return render_template('TwittMap.html', locs=[])
    else:
        return render_template('TwittMap.html', locs=[])


@app.route('/local', methods=['GET','POST'])
def tweetmap2():
    if request.method == 'POST':
        lat = request.args['lat']
        lon = request.args['lon']
        print(lat)
        print(lon)
        return render_template('TwittMap.html', locs=[lat, lon])
    else:
        return render_template('TwittMap.html', locs=[])


if __name__ == "__main__":
    app.run(debug=True)
