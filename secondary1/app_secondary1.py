from flask import Flask

from views import secondary1

app_secondary1 = Flask(__name__)

# Register the Blueprint with the app
app_secondary1.register_blueprint(secondary1, url_prefix="/secondary1")


@app_secondary1.route("/")
def app_secondary1_route():
    return "This is Secondary1 Service"


if __name__ == "__main__":
    app_secondary1.run(debug=True, host="0.0.0.0")
