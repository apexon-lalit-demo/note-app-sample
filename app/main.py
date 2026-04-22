"""Notes Web App — sample app for Vibe Coder deployment."""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

notes: dict[str, dict] = {}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "notes-app"})


@app.route("/")
def index():
    sorted_notes = sorted(notes.values(), key=lambda n: n["created_at"], reverse=True)
    return render_template("index.html", notes=sorted_notes)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    color = request.form.get("color", "#ffd43b")
    if title:
        nid = str(uuid.uuid4())[:8]
        notes[nid] = {
            "id": nid,
            "title": title,
            "body": body,
            "color": color,
            "created_at": datetime.utcnow().isoformat(),
        }
    return redirect(url_for("index"))


@app.route("/delete/<nid>")
def delete(nid):
    notes.pop(nid, None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
