from flask import Flask

from views import master

app_master = Flask(__name__)

# Register the Blueprint with the app
app_master.register_blueprint(master, url_prefix="/master")


@app_master.route("/")
def app_master_route():
    return "This is Master Service"


if __name__ == "__main__":
    app_master.run(debug=True, port=5001)
