from flask import Blueprint, render_template, flash, session, redirect, url_for

from app.models.admin_model import Categories, Services
from app.utils.auth import login_required

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/hizmetler")
def service_categories():
    categories_model = Categories()

    status, msgordatas = categories_model.get_all_by_type("service")

    if not status:
        flash(msgordatas, "danger")
        return redirect(url_for("main.index"))

    return render_template("service_categories.html", datas = msgordatas)

@main.route("/hizmetler/<category_slug>")
def services(category_slug):
    service_model = Services()
    categories_model = Categories()

    status, messageorid = categories_model.get_id_by_slug(category_slug)

    if not status:
        flash(messageorid, "danger")
        return redirect(url_for("main.index"))
    
    service_status, msgordatas = service_model.get_all_by_category_id(messageorid)

    if not service_status:
        flash(msgordatas, "danger")
        return redirect(url_for("main.index"))
    
    return render_template("services.html", datas = msgordatas, category_slug = category_slug)

@main.route("/h/<service_category>/<service>")
def service_categories_type(service_category, service):
    service_model = Services()

    status, msgordata = service_model.get_by_slug(service)

    if not status:
        flash(msgordata, "danger")
        return redirect(url_for("main.services", category_slug = service_category)) 
    
    return render_template("service.html", data = msgordata, service_category = service_category)

@main.route("/projeler")
def project_categories():
    categories_model = Categories()

    status, msgordatas = categories_model.get_all_by_type("project")

    if not status:
        flash(msgordatas, "danger")
        return redirect(url_for("main.index"))

    return render_template("project_categories.html", datas = msgordatas)

@main.route("/contact")
def contact():
    return render_template("contact.html")