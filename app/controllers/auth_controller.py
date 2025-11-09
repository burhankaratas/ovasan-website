from flask import Blueprint, render_template, request, flash, redirect, url_for, session

from app.utils.auth import verify_recaptcha, user_authentication

auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        token = request.form.get("g-recaptcha-response")

        status, message = verify_recaptcha(token)

        if not status:
            flash("Recaptcha doğrulaması başarısız.", "danger")
            return redirect(url_for("auth.login"))
        
        login_status, login_message = user_authentication(username, password)

        if not login_status:
            flash(login_message, "danger")
            return redirect(url_for("auth.login"))
        
        session["logged_in"] = True
        
        flash(login_message, "success")
        return redirect(url_for("admin.admin_index"))
            
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))