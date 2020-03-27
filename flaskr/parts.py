from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from werkzeug.exceptions import abort

import os
import shutil

from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.classxml import parse_hierarchy_xml,get_class_string,get_linear_class_list

bp = Blueprint("parts", __name__)


@bp.route("/")
def index():
    """Give the menu of choices"""
    # Gather summary statistics
    db = get_db()
    tablename = "parts"+g.user['username']
    parts = db.execute(
        "SELECT qty, cost FROM " + tablename,
    ).fetchall()
    summary = dict()
    num = 0
    value = 0.0
    for part in parts:
        num = num + int(part['qty'])
        if len(part['cost']) > 0:
            value = value + (part['qty'] * float(part['cost']))
    summary['total_num'] = str(num)
    summary['total_value'] = '%.2f' % value
    return render_template("parts/index.html", summary=summary)

@bp.route("/browse")
@login_required
def browse():
    """Show all the posts, most recent first."""
    db = get_db()
    tablename = "parts"+g.user['username']
    parts = db.execute(
        "SELECT id, type, class, qty, pkg, manuf, partnum, cost, location, description, notes, url FROM " + tablename,
    ).fetchall()
    # parse the class xml file before get_class_string is called in the template
    parse_hierarchy_xml('./flaskr/static/class.xml')
    return render_template("parts/browse.html", parts=parts, str_type=str, get_class_string=get_class_string)

def get_part(id):
    """Get a part by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of part to get
    :return: the part
    :raise 404: if a part with the given id doesn't exist
    """
    tablename = "parts"+g.user['username']
    part = (
        get_db()
        .execute(
            "SELECT id, type, class, qty, pkg, manuf, partnum, cost, location, description, notes, url"
            " FROM " + tablename + " WHERE id = ?",
            (id,),
        )
        .fetchone()
    )

    if part is None:
        abort(404, "Part id {0} doesn't exist.".format(id))

    return part


@bp.route("/add", methods=("GET", "POST"))
@login_required
def add():
    """Add a new part for the current user."""
    if request.method == "POST":
        ptype = request.form['type']
        manuf = request.form['manuf']
        partnum = request.form['partnum']
        pkg = request.form['pkg']
        description = request.form['description']
        pclass = request.form['class']
        qty = request.form['qty']
        location = request.form['location']
        cost = request.form['cost']
        notes = request.form['notes']
        url = request.form['url']
        error = None

        if not ptype:
            error = "Type is required."
        if not qty:
            error = "Quantity is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            tablename = "parts"+g.user['username']
            db.execute(
                "INSERT INTO " + tablename +" (type, class, qty, pkg, manuf, partnum, cost, location, description, notes, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ptype, pclass, qty, pkg, manuf, partnum, cost, location, description, notes, url),
            )
            db.commit()
            flash("New part added to database.")
            return redirect(url_for("parts.browse"))

    parse_hierarchy_xml('./flaskr/static/class.xml')
    class_list = get_linear_class_list()
    return render_template("parts/add.html", class_list=class_list)


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    part = get_part(id)

    if request.method == "POST":
        ptype = request.form['type']
        manuf = request.form['manuf']
        partnum = request.form['partnum']
        pkg = request.form['pkg']
        description = request.form['description']
        pclass = request.form['class']
        qty = request.form['qty']
        location = request.form['location']
        cost = request.form['cost']
        notes = request.form['notes']
        url = request.form['url']
        if 'datafile' in request.files:
            datafile = request.files['datafile']
        else:
            datafile = None
        error = None

        if not ptype:
            error = "Type is required."
        if not qty:
            error = "Quantity is required."

        if error is not None:
            flash(error)
        else:
            if datafile and datafile.filename != '':
                # copy datasheet to data directory and set URL to resulting location
                src = os.path.join(current_app.config["UPLOAD_DIR"], datafile.filename)
                dest = os.path.join(current_app.config["DATA_DIR"], datafile.filename)
                try:
                    datafile.save(src)
                    shutil.move(src, dest)
                    url = url_for('send_datasheet', path=datafile.filename)
                except OSError:
                    flash("File operation failed")
            db = get_db()
            tablename = "parts"+g.user['username']
            db.execute(
                "UPDATE " + tablename + " SET type = ?, class = ?, qty = ?, pkg = ?, manuf = ?, partnum = ?, cost = ?, location = ?, description = ?, notes = ?, url = ? WHERE id = ?", 
                (ptype, pclass, qty, pkg, manuf, partnum, cost, location, description, notes, url, id)
            )
            db.commit()
            return redirect(url_for("parts.browse"))

    parse_hierarchy_xml('./flaskr/static/class.xml')
    class_list = get_linear_class_list()
    return render_template("parts/update.html", part=part, class_list=class_list)

@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_part(id)
    db = get_db()
    tablename = "parts"+g.user['username']
    db.execute("DELETE FROM " + tablename + " WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("parts.browse"))
