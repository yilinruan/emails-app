import os
from flask import Flask, request, send_from_directory
from datetime import datetime
from base64 import urlsafe_b64decode
from pymongo import MongoClient

app = Flask(__name__)

# ✅ Updated MongoDB Atlas connection string (Added `email_tester_db` at the end)
MONGO_URI = "mongodb+srv://ss1156161413:testemail123@cluster0.xg8fd.mongodb.net/email_tester_db?retryWrites=true&w=majority&appName=Cluster0"

# ✅ Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["email_tester_db"]  # Now it connects to the correct database
visits_collection = db["Visits"]  # MongoDB will create this automatically

@app.route('/')
def index():
    ip_addr = request.remote_addr
    args = request.args
    name = args.get("name", default="")

    if 'refer_code' in args:
        name = urlsafe_b64decode(str.encode(args.get('refer_code'))).decode()

    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # ✅ Store visitor data in MongoDB (No schema needed)
    visits_collection.insert_one({"ip": ip_addr, "name": name, "datetime": now})

    return send_from_directory('static', 'index.html')

@app.route('/getRecords')
def getRecords():
    visits = list(visits_collection.find({}, {"_id": 0}))  # Hide MongoDB's `_id`
    return '<br/>'.join([str(v) for v in visits])

@app.route('/<path:path>')
def other_rsc(path):
    return send_from_directory('static', path)

# ✅ Use Heroku's port if available
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
