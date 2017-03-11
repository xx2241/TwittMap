from flask import *
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
	
	return render_template('test.html')


if __name__ == "__main__":
	app.run(debug=True)