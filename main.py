from flask import Flask, request, send_file, send_from_directory
from datetime import datetime
from base64 import urlsafe_b64decode
import sqlite3
db = sqlite3.connect("records.db")
db.execute("CREATE TABLE IF NOT EXISTS Visits(ip text, name text, datetime text)")
db.commit()
db.close()

app = Flask(__name__)


@app.route('/')
def index():
  db = sqlite3.connect("records.db")
  cur = db.cursor()
  ip_addr = request.remote_addr
  args = request.args
  name = args.get("name", default="")
  if 'refer_code' in args:
    name = urlsafe_b64decode(str.encode(args.get('refer_code'))).decode()
  now = datetime.now()
  now = now.strftime("%m/%d/%Y, %H:%M:%S")

  params = [ip_addr, name, now]
  print(params)
  cur.execute("INSERT INTO Visits(ip, name, datetime) VALUES (?, ?, ?)", params)
  cur.close()
  db.commit()
  db.close()
  return send_from_directory('static', 'index.html')


"""
@app.route('/record', methods=['POST'])
def record():
  return 'Hello, World!' 
  """




@app.route('/getRecords')
def getRecords():
  db = sqlite3.connect("records.db")
  cur = db.cursor()
  res = cur.execute("SELECT ip, name, datetime FROM Visits")
  visits = res.fetchall()
  db.close()
  return '<br/>'.join([str(v) for v in visits])


@app.route('/<path:path>')
def other_rsc(path):
  print('rsc')
  return send_from_directory('static', path)

app.run(host='0.0.0.0', port=5000)