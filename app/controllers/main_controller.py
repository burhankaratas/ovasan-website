import os
from flask import Blueprint, render_template, flash, session, redirect, url_for, request, send_from_directory, current_app

from app.models.admin_model import Categories, Services, CareerApplications
from app.utils.auth import login_required, verify_recaptcha

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

    random_status, random_services = service_model.get_random_with_category(
        limit=4,
        exclude_id=msgordata.get("id")
    )
    if not random_status:
        random_services = []
    
    return render_template(
        "service.html",
        data=msgordata,
        service_category=service_category,
        other_services=random_services
    )

@main.route("/projeler")
def project_categories():
    categories_model = Categories()

    status, msgordatas = categories_model.get_all_by_type("project")

    if not status:
        flash(msgordatas, "danger")
        return redirect(url_for("main.index"))

    return render_template("project_categories.html", datas = msgordatas)

@main.route("/projects")
def projects():
    return render_template("projects.html")

@main.route("/projects/<slug>")
def project_detail(slug):
    from app.data.projects_data import PROJECTS, PROJECTS_LIST

    project = PROJECTS.get(slug)
    if not project:
        flash("Proje bulunamadı.", "danger")
        return redirect(url_for("main.projects"))

    docs_base = os.path.normpath(os.path.join(current_app.root_path, '..', 'docs'))
    folder_path = os.path.join(docs_base, project["folder"])

    images = []
    if os.path.isdir(folder_path):
        allowed_ext = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.jfif')
        for f in sorted(os.listdir(folder_path)):
            if f.lower().endswith(allowed_ext):
                images.append(f)

    return render_template(
        "project_detail.html",
        project=project,
        slug=slug,
        images=images,
        all_projects=PROJECTS_LIST,
    )

@main.route("/docs-media/<path:filepath>")
def docs_media(filepath):
    docs_base = os.path.normpath(os.path.join(current_app.root_path, '..', 'docs'))
    directory = os.path.join(docs_base, os.path.dirname(filepath))
    filename  = os.path.basename(filepath)
    return send_from_directory(directory, filename)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        token = request.form.get("g-recaptcha-response")
        status, _message = verify_recaptcha(token)
        if not status:
            flash("Recaptcha doğrulaması başarısız.", "danger")
            return redirect(url_for("main.contact"))

        form_data = {
            "kurum_name": request.form.get("kurum_name", "").strip(),
            "name": request.form.get("name", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "email": request.form.get("email", "").strip(),
            "service": request.form.get("service", "").strip(),
            "message": request.form.get("message", "").strip(),
        }
        uploaded_file = request.files.get("file")

        try:
            from app.utils.mail import send_mail
        except Exception:
            send_mail = None

        if send_mail and send_mail(form_data, uploaded_file):
            flash("Mesajınız başarıyla gönderildi.", "success")
        else:
            flash("Mesajınız gönderilemedi. Lütfen tekrar deneyin.", "danger")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

@main.route("/kariyer", methods=["GET", "POST"])
def career():
    if request.method == "POST":
        token = request.form.get("g-recaptcha-response")
        status, _message = verify_recaptcha(token)
        if not status:
            flash("Recaptcha doğrulaması başarısız.", "danger")
            return redirect(url_for("main.career"))

        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        age = request.form.get("age", "").strip()
        email = request.form.get("email", "").strip()
        education = request.form.get("education", "").strip()
        field = request.form.get("field", "").strip()
        interests = request.form.getlist("interests")

        interest_text = ", ".join([i.strip() for i in interests if i.strip()])

        career_model = CareerApplications()
        status, message = career_model.create(
            first_name,
            last_name,
            age,
            email,
            education,
            field,
            interest_text
        )

        if status:
            flash(message, "success")
        else:
            flash(message, "danger")
        return redirect(url_for("main.career"))

    return render_template("career.html")
