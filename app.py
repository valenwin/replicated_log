from flask import Flask
import threading

from master.views import master
from secondary1.views import secondary1
from secondary2.views import secondary2

app_master = Flask(__name__)
app_secondary1 = Flask(__name__)
app_secondary2 = Flask(__name__)

app_master.register_blueprint(master, url_prefix="/master")
app_secondary1.register_blueprint(secondary1, url_prefix="/secondary1")
app_secondary2.register_blueprint(secondary2, url_prefix="/secondary2")


@app_master.route("/")
def app_master_route():
    return "This is Master Service"


@app_secondary1.route("/")
def app_secondary1_route():
    return "This is Secondary1 Service"


@app_secondary2.route("/")
def app_secondary2_route():
    return "This is Secondary2 Service"


if __name__ == "__main__":
    # Start the Flask apps in separate threads
    thread1 = threading.Thread(target=app_master.run, kwargs={"port": 5001})
    thread2 = threading.Thread(target=app_secondary1.run, kwargs={"port": 5002})
    thread3 = threading.Thread(target=app_secondary2.run, kwargs={"port": 5003})

    thread1.start()
    thread2.start()
    thread3.start()
