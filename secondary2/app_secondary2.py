from flask import Flask

from views import secondary2

app_secondary2 = Flask(__name__)

# Register the Blueprint with the app
app_secondary2.register_blueprint(secondary2, url_prefix="/secondary2")


@app_secondary2.route("/")
def app_secondary2_route():
    return "This is Secondary2 Service"


if __name__ == "__main__":
    app_secondary2.run(debug=True, port=5003)
