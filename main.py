import os
import base64
from flask import Flask, request, send_from_directory
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__, static_folder="static")

# ✅ MongoDB Connection
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://ss1156161413:testemail123@cluster0.xg8fd.mongodb.net/email_tester_db?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["email_tester_db"]
clicks_collection = db["EmailClicks"]  # ✅ Store email clicks

@app.route('/')
def track_click():
    ip_addr = request.remote_addr
    args = request.args

    # ✅ Check if `refer_code` exists, otherwise do NOT record
    if 'refer_code' not in args or not args.get('refer_code'):
        print(f"⚠️ Ignoring request from {ip_addr} (No refer_code)")
        return send_from_directory('static', 'index.html')  # Serve page but don't log

    try:
        email = base64.urlsafe_b64decode(args.get('refer_code')).decode().strip().lower()
        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        # ✅ Store valid click data in MongoDB
        click_data = {"ip": ip_addr, "email": email, "datetime": now}
        clicks_collection.insert_one(click_data)

        print(f"✅ Email Click Logged: {click_data}")  # Debugging info

    except Exception:
        print(f"⚠️ Invalid refer_code detected, ignoring request from {ip_addr}")

    return send_from_directory('static', 'index.html')

@app.route('/getClickRecords')
def get_click_records():
    clicks = list(clicks_collection.find({}, {"_id": 0}))  # Hide MongoDB's `_id`
    return '<br/>'.join([str(c) for c in clicks])

# ✅ Use Heroku's dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
