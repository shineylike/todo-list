"""Rutele aplicației web To-Do List."""

import os
import secrets

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from todo import add_task, delete_task, load_tasks, toggle_task


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)


@app.route("/", methods=["GET"])
def index():
    """Afișează sarcinile salvate."""
    return render_template("index.html", tasks=load_tasks())


@app.route("/add", methods=["POST"])
def add():
    """Adaugă sarcina trimisă din formular."""
    title = request.form.get("title", "")
    if not title.strip():
        flash("Sarcina nu poate fi goală", "error")
        return redirect(url_for("index"))

    add_task(title)
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle(task_id):
    """Inversează starea de finalizare a unei sarcini."""
    try:
        toggle_task(task_id)
    except (LookupError, ValueError):
        abort(404)
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    """Șterge sarcina indicată."""
    try:
        delete_task(task_id)
    except (LookupError, ValueError):
        abort(404)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
