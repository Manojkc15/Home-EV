import pymongo
from flask import Flask, jsonify, request, session, redirect, url_for
import uuid
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
# scheduler=APScheduler()


url = "mongodb+srv://user1234:59dLdTzaKaqimTt@user.vl67u.mongodb.net/user_login_system?retryWrites=true&w=majority"
client = pymongo.MongoClient(url)
db = client.providers


class provider:
    def start_session(self, provider):
        print(provider)
        del provider['password']
        session['logged_in'] = True
        session['provider'] = provider
        return jsonify(provider), 200

    def apply(self, name, email, password,mob_no,lat,long):
        # print(request.form)
        print("dfg")
        # Create the provider object
        provider = {
            "_id": uuid.uuid4().hex,
            "p_name": name,
            "p_email": email,
            "mobile_no": mob_no,
            "latitude": lat,
            "longitude": long,
            "password": password
        }
        print("dfg")
        # Encrypt the password
        provider['password'] = pbkdf2_sha256.encrypt(provider['password'])

        # Check for existing email address
        if db.provide.find_one({"p_email": provider['p_email']}):
            return jsonify({"error": "Email address already in use"}), 400
        print("dfg")
        if db.provide.insert_one(provider):
            self.start_session(provider)
            return jsonify({"message":"Succesfully signed up"})

        return jsonify({"error": "Signup failed"}), 400

    def login(self, email, password):
        print("Hello", email, password)

        provider = db.provide.find_one({
            "p_email": email
        })
        print(provider)
        # print(pbkdf2_sha256.verify(password, provider['password']))
        if provider and pbkdf2_sha256.verify(password, provider['password']):
            print("Login sucessful")
            self.start_session(provider)
            return jsonify({"message":"Sucessfully Logged in"})

        return jsonify({"error": "Invalid login credentials"}), 401


@app.route('/')
def home():
    return  "Hello World..........."


@app.route('/home')
def test():
    return  "Hello ..."


@app.route('/provider/apply', methods=['POST'])
def apply():
    body = request.json
    print(body)
    print(body['email'], body['password'])
    return provider().apply(body['name'], body['email'], body['password'],body['mob_no'],body['lat'],body['long'])


@app.route('/provider/signout')
def signout():
    return provider().signout()


@app.route('/provider/login', methods=['POST'])
def login():
    if request.method == 'POST':
        body = request.json
        print(body)
        return  provider().login(body['email'], body['password'])


if __name__ == "__main__":
    # TODO Valid return statements for all routes
    # TODO to filter correct values from database
    app.run(debug=True)