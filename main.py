from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, Google Cloud Run!"

if __name__ == "__main__":
    # Cloud Run expects the app to run on 0.0.0.0 and port 8080
    app.run(host="0.0.0.0", port=8080)