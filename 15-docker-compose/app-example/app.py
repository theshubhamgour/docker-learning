from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return f"Environment : {os.getenv('ENV')}"

app.run(host="0.0.0.0", port=5002)
