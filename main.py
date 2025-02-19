import os
import base64
from flask import Flask, request, send_from_directory
from datetime import datetime
from pymongo import MongoClient

app = Flask(__name__, static_folder="static")

# ✅ Use MongoDB connection string from Heroku ENV variable
MONGO_URI = os.getenv("MONGODB_URI", "mongodb+srv://ss1156161413:testemail123@cluster0.xg8fd.mongodb.net/email_tester_db?retryWrites=true&w=majority&appName=Cluster0")

# ✅ Connect to MongoDB
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["email_tester_db"]
clicks_collection = db["EmailClicks"]  # ✅ Track email clicks

# ✅ Fix: Serve Static Files (Images, CSS, JS)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory("static", filename)

@app.route('/')
def track_click():
    ip_addr = request.remote_addr  # ✅ Get user's IP address
    args = request.args
    email = None

    # ✅ Decode email from `refer_code` (if present)
    if 'refer_code' in args:
        try:
            decoded_email = base64.urlsafe_b64decode(args.get('refer_code')).decode().strip().lower()
            email = decoded_email  # ✅ Standardize email (lowercase & stripped)
        except Exception:
            email = "Unknown"

    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # ✅ Store click data in MongoDB
    click_data = {"ip": ip_addr, "email": email, "datetime": now}
    clicks_collection.insert_one(click_data)

    print(f"✅ Email Click Logged: {click_data}")  # Debugging info

    return send_from_directory('static', 'index.html')

@app.route('/getClickRecords')
def get_click_records():
    clicks = list(clicks_collection.find({}, {"_id": 0}))  # Hide MongoDB's `_id`
    return '<br/>'.join([str(c) for c in clicks])

# ✅ Use Heroku's dynamic port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
