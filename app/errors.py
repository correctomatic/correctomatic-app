from flask import render_template

def page_not_found(e):
    return render_template("errors/404.html.j2"), 404

def register_errors(app):
    app.register_error_handler(404, page_not_found)

