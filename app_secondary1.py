from flask import Flask

from secondary1.views import secondary1

app_secondary1 = Flask(__name__)

# Register the Blueprint with the app
app_secondary1.register_blueprint(secondary1, url_prefix="/secondary1")


@app_secondary1.route("/")
def hello_world1():  # put application's code here
    return "Hello World!"


if __name__ == "__main__":
    app_secondary1.run(debug=True, port=5002)
