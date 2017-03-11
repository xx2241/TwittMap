from flask import *
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def hello():
	return render_template('test.html')

@app.route('/',methods=['GET'])
def search():
	keyword = request.args.get('keyword')
	print(keyword)


if __name__ == "__main__":
	app.run(debug=True)