from flask import Flask, request
import ml_application as ml

app = Flask(__name__)

# Going from Chatbot to Model
@app.route('/predict', methods=['POST'])
def post_from_application():
    aList = eval(request.form.getlist('list')[0])
    predict = ml.predict(aList)
    return predict

if __name__ == '__main__':
    app.run(debug=True)
