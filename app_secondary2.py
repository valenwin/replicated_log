from flask import Flask

from secondary2.views import secondary2

app_secondary2 = Flask(__name__)

# Register the Blueprint with the app
app_secondary2.register_blueprint(secondary2, url_prefix='/secondary2')


@app_secondary2.route('/')
def hello_world2():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app_secondary2.run(debug=True, port=5003)
