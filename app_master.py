from flask import Flask

from master.views import master

app_master = Flask(__name__)

# Register the Blueprint with the app
app_master.register_blueprint(master, url_prefix='/master')


@app_master.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app_master.run(debug=True, port=5000)
