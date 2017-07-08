from flask import Flask, request
import ml_application as ml

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def post_from_application():
    aList = eval(request.form.getlist('list')[0])
    predict = ml.predict(aList)
    return predict

@app.route('/posting', methods=['POST'])
def posting():

    return 

if __name__ == '__main__':
    app.run(debug=True)

# Test the get - curl -X GET http://localhost:5000/placeholder_get
# test the post curl -d "test" -X POST http://localhost:5000/placeholder_post