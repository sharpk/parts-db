from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.classxml import parse_hierarchy_xml,get_class_string,get_linear_class_list

bp = Blueprint("parts", __name__)


@bp.route("/")
def index():
	"""Give the menu of choices"""
	return render_template("parts/index.html")

@bp.route("/browse")
@login_required
def browse():
    """Show all the posts, most recent first."""
    db = get_db()
    tablename = "parts"+g.user['username']
    parts = db.execute(
        "SELECT type, class, qty, pkg, manuf, partnum, cost, location, description, notes, url FROM " + tablename,
    ).fetchall()
    # parse the class xml file before get_class_string is called in the template
    parse_hierarchy_xml('./flaskr/static/class.xml')
    return render_template("parts/browse.html", parts=parts, str_type=str, get_class_string=get_class_string)

def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


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
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("parts.browse"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("parts.browse"))
