
from flask import Flask
app = Flask(__name__)

from flask import request
from SpamClassifier import *
@app.route('/smish')
def api_hello():
    if 'message' in request.args:
		result=func(request.args['message'])
		return result
    else:
        return 'you did not enter any message!'

if __name__ == '__main__' :
	app.run()