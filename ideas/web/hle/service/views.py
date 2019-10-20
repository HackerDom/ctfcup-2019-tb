from flask import redirect, render_template, request, session, url_for, make_response
from functools import wraps
from .wsgi import app, SECRET, ADMIN_LOGIN, FLAG
from .hasher import calculate_hash

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_hash = request.cookies.get("auth_hash")
        login = request.cookies.get("login")
        if not auth_hash or not login:
            return redirect(url_for("auth", next=request.url))

        calculdated_hash = calculate_hash(SECRET + login)
        if calculdated_hash != auth_hash:
            return redirect(url_for("auth", next=request.url))

        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
@auth_required
def index() -> str:
    message = FLAG
    if ADMIN_LOGIN.lower() not in request.cookies.get("login").lower():
        message = "Must be admin to view flag"
    return render_template("index.html", message=message)


@app.route('/login', methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        login = request.form["login"]

        if ADMIN_LOGIN in login:
            return render_template("login.html", error="Do you realy think this is so easy???")
        resp = make_response(redirect(url_for("index")))
        resp.set_cookie("login", login)
        resp.set_cookie("auth_hash", calculate_hash(SECRET + login))
        return resp

    error = request.args.get("error")
    return render_template("login.html", error=error)
