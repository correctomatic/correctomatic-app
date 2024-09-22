from flask import render_template

def page_not_found(e):
    return render_template("errors/404.html.j2"), 404

def forbidden(e):
    return render_template('errors/403.html.j2'), 403

def register_errors(app):
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)

