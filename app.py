from flask import Flask, jsonify
from mongoengine import connect, Document, StringField

import os

app = Flask(__name__)

# Local MongoDB for development
MONGODB_URI =  os.environ.get("AZURE_COSMOS_CONNECTIONSTRING") or os.environ.get("MONGODB_URI") 

connect(host=MONGODB_URI)

class Note(Document):
    title = StringField(required=True)
    body = StringField()

# Seed at startup
if Note.objects.count() == 0:
    Note(title="Local startup note", body="Hello from local MongoDB").save()

@app.route("/")
def health():
    return jsonify({"ok": True})

@app.route("/notes")
def list_notes():
    return jsonify([{"id": str(n.id), "title": n.title, "body": n.body} for n in Note.objects])

