import datetime
from dataserv.Farmer import Farmer, db
from flask import Flask, make_response


# Initialize the Flask application
app = Flask(__name__)


# Routes
@app.route('/')
def index():
    return "Hello World."


@app.route('/api/register/<btc_addr>', methods=["GET"])
def register(btc_addr):
    # create Farmer object to represent user
    user = Farmer(btc_addr)

    # error template
    error_msg = "Registration Failed: {0}"

    # attempt to register the farmer/farming address
    try:
        user.register()
        return make_response("User registered.", 200)
    except ValueError:
            msg = "Invalid BTC Address."
            return make_response(error_msg.format(msg), 400)
    except LookupError:
            msg = "Address Already Is Registered."
            return make_response(error_msg.format(msg), 409)


@app.route('/api/ping/<btc_addr>', methods=["GET"])
def ping(btc_addr):
    # create Farmer object to represent user
    user = Farmer(btc_addr)

    # error template
    error_msg = "Ping Failed: {0}"

    # attempt to register the farmer/farming address
    try:
        user.ping()
        return make_response("Ping Accepted.", 200)
    except ValueError:
        msg = "Invalid BTC Address."
        return make_response(error_msg.format(msg), 400)
    except LookupError:
        msg = "Farmer not found."
        return make_response(error_msg.format(msg), 404)


@app.route('/api/online', methods=["GET"])
def online():
    # maximum number of minutes since the last check in for
    # the farmer to be considered an online farmer
    online_time = 15  # minutes

    current_time = datetime.datetime.utcnow()
    time_ago = current_time - datetime.timedelta(minutes=online_time)

    online_farmers = db.session.query(Farmer).filter(Farmer.last_seen > time_ago).all()
    output = ""
    for farmer in online_farmers:
        seconds_ago =  (current_time - farmer.last_seen).seconds
        if seconds_ago < 60:
            output += "{0} {1} seconds<br/>".format(str(farmer.btc_addr), seconds_ago)
        else:
            output += "{0} {1} minute(s)<br/>".format(str(farmer.btc_addr), int(seconds_ago/60))
    return output

if __name__ == '__main__':  # pragma: no cover
    # Create Database
    db.create_all()

    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
