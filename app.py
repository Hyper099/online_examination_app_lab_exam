import os
from secrets import compare_digest, token_hex

from flask import Flask, abort, redirect, render_template, request, session, url_for
from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash, generate_password_hash

from db import users
from questions import QUESTIONS
from result_calculation import calculate_score

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or token_hex(32)
app.config.update(SESSION_COOKIE_SAMESITE="Lax", MAX_CONTENT_LENGTH=16 * 1024)


@app.before_request
def protect_forms():
    if "csrf_token" not in session:
        session["csrf_token"] = token_hex(32)
    if request.method == "POST":
        submitted = request.form.get("csrf_token", "")
        if not compare_digest(submitted.encode(), session["csrf_token"].encode()):
            abort(400)


@app.get("/")
def index():
    return redirect(url_for("exam" if "username" in session else "login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        if not 1 <= len(username) <= 40 or not 8 <= len(password) <= 128:
            error = "Enter a username of 1–40 characters and a password of 8–128 characters."
        else:
            try:
                users.insert_one({"_id": username, "password_hash": generate_password_hash(password)})
            except DuplicateKeyError:
                error = "That username is already registered."
            else:
                return redirect(url_for("login"))
    return render_template("account.html", title="Register", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = users.find_one({"_id": username})
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["username"] = username
            return redirect(url_for("exam"))
        error = "Invalid username or password."
    return render_template("account.html", title="Log in", error=error)


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "username" not in session:
        return redirect(url_for("login"))

    error = None
    if request.method == "POST":
        try:
            answers = [int(request.form.get(f"q{number}", "")) for number in range(1, len(QUESTIONS) + 1)]
            score = calculate_score(answers, [correct for _, _, correct in QUESTIONS])
        except ValueError:
            error = "Choose one valid option for every question."
        else:
            users.update_one(
                {"_id": session["username"]},
                {"$set": {"result": {"score": score, "total": len(QUESTIONS)}}},
            )
            return redirect(url_for("results"))

    questions = [(prompt, options) for prompt, options, _ in QUESTIONS]
    return render_template("exam.html", questions=questions, error=error)


@app.get("/results")
def results():
    if "username" not in session:
        return redirect(url_for("login"))
    user = users.find_one({"_id": session["username"]}, {"result": 1})
    return render_template("results.html", result=(user or {}).get("result"))
