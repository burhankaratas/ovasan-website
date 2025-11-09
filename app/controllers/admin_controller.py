from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import os 

from app.utils.auth import login_required
from app.utils.admin import save_file

from app.models.admin_model import Contact, Categories, Services


admin = Blueprint('admin', __name__, url_prefix="/admin")


MESSAGES_PER_PAGE = 5 

UPLOAD_FOLDER = "app/static/img/sliders"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_pagination(current_page, total_messages, max_links=7):
    total_pages = (total_messages + MESSAGES_PER_PAGE - 1) // MESSAGES_PER_PAGE
    pages = []

    if total_pages <= max_links:
        pages = list(range(1, total_pages+1))
    else:
        if current_page <= 4:
            pages = [1, 2, 3, 4, 5, '...', total_pages]
        elif current_page >= total_pages - 3:
            pages = [1, '...', total_pages-4, total_pages-3, total_pages-2, total_pages-1, total_pages]
        else:
            pages = [1, '...', current_page-1, current_page, current_page+1, '...', total_pages]

    return pages, total_pages


@admin.route("/")
@login_required
def admin_index():
    return render_template("admin/index.html")

@admin.route('/slider', methods=['GET', 'POST'])
def slider_panel():
    if request.method == "GET":
         return render_template('admin/slider.html')
    
    elif request.method == 'POST':
        try:
            slider_number = int(request.form['slider_number'])
            file = request.files['file']

            if slider_number not in range(1, 6):
                flash("Slider numarası 1 ile 5 arasında olmalı.", "danger")
                return redirect(url_for('admin.slider_panel'))

            if file and allowed_file(file.filename):
                filename = f"slider{slider_number}.png"
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                flash(f"Slider {slider_number} başarıyla güncellendi!", "success")
            else:
                flash("Lütfen geçerli bir resim dosyası yükleyin.", "danger")

        except Exception as e:
            flash(f"Hata: {e}", "danger")

        return redirect(url_for('admin.slider_panel'))

@admin.route("/contact")
@login_required
def admin_contact():
    page = request.args.get("contact", 1, type=int)
    
    contact_model = Contact()
    total_messages = contact_model.count() 
    messages_page = contact_model.get_all(page=page, per_page=MESSAGES_PER_PAGE)

    pages, total_pages = get_pagination(page, total_messages)
    print(pages)

    return render_template(
        "admin/contact.html",
        messages=messages_page,
        pages=pages,
        current_page=page
    )

@admin.route("/categories")
@login_required
def admin_categories():
    categories_model = Categories()

    status, msgordatas = categories_model.get_all()

    if not status:
        flash(msgordatas, "danger")
        return redirect(url_for("admin.admin_index"))

    return render_template("/admin/categories.html", datas = msgordatas)

@admin.route("/categories/edit", methods = ["POST"])
@login_required
def admin_categories_edit():
    if request.method == "POST":
        category_id = request.form.get("category_id")
        name = request.form.get("name")
        slug = request.form.get("slug")
        category_type = request.form.get("category_type")

        categories_model = Categories()

        status, message = categories_model.edit(name, slug, category_type, category_id)

        if not status:
            flash(message, "danger")
            return redirect(url_for("admin.admin_categories"))
        
        flash(message, "success")
        return redirect(url_for("admin.admin_categories"))
    
@admin.route("/categories/delete", methods = ["POST"])
@login_required
def admin_categories_delete():
    if request.method == "POST":
        category_id = request.form.get("category_id")

        categories_model = Categories()

        status, message = categories_model.delete(category_id)

        if not status:
            flash(message, "danger")
            return redirect(url_for("admin.admin_categories"))
        
        flash(message, "success")
        return redirect(url_for("admin.admin_categories"))
    
@admin.route("/categories/create", methods = ["POST"])
@login_required
def admin_categories_create():
    if request.method == "POST":
        name = request.form.get("name")
        slug = request.form.get("slug")
        category_type = request.form.get("category_type")

        image = request.files["image"]

        image_status, file_name = save_file(image, "categories")

        if not image_status:
            flash(file_name, "danger")
            return redirect(url_for("admin.admin_categories"))
        
        categories_model = Categories()

        status, message = categories_model.create(name, slug, category_type, file_name)

        if not status:
            flash(message, "danger")
            return redirect(url_for("admin.admin_categories"))
        
        flash(message, "success")
        return redirect(url_for("admin.admin_categories"))

@admin.route("/services")
@login_required
def admin_services():
    categories_model = Categories()
    services_model = Services()

    status_categories, categories = categories_model.get_all_by_type("service")
    status_services, services = services_model.get_all()

    if not status_categories:
        flash(categories, "danger")
        return redirect(url_for("admin.admin_index"))
    
    if not status_services:
        flash(services, "danger")
        return redirect(url_for("admin.admin_index"))

    return render_template("/admin/services.html", categories = categories, datas = services)

@admin.route("/services/create", methods=["POST"])
@login_required
def admin_services_create():
    if request.method == "POST":
        service_data = {
            "category_id": request.form.get("category_id"),
            "title": request.form.get("title"),
            "slug": request.form.get("slug"),
            "main_heading": request.form.get("main_heading"),
            "subtitle1": request.form.get("subtitle1"),
            "subtitle2": request.form.get("subtitle2"),
            "subtitle3": request.form.get("subtitle3"),
            "subtitle4": request.form.get("subtitle4"),
            "text1": request.form.get("text1"),
            "text2": request.form.get("text2"),
            "text3": request.form.get("text3"),
            "text4": request.form.get("text4"),
            "text5": request.form.get("text5"),
            "text6": request.form.get("text6"),
            "text7": request.form.get("text7"),
            "image": None
        }

        if "image" in request.files:
            image = request.files["image"]
            image_status, file_name = save_file(image, "services")
            if not image_status:
                flash(file_name, "danger")
                return redirect(url_for("admin.admin_services"))
            service_data["image"] = file_name

        services_model = Services()
        status, message = services_model.create(service_data)

        if not status:
            flash(message, "danger")
        else:
            flash(message, "success")

        return redirect(url_for("admin.admin_services"))
    
@admin.route("/services/delete", methods = ["POST"])
@login_required
def admin_services_delete():
    if request.method == "POST":
        service_id = request.form.get("service_id")

        service_model = Services()

        status, message = service_model.delete(service_id)

        if not status:
            flash(message, "danger")
            return redirect(url_for("admin.admin_services"))
        
        flash(message, "success")
        return redirect(url_for("admin.admin_services"))

@admin.route("/projects")
@login_required
def admin_projects():
    return render_template("/admin/projects.html")