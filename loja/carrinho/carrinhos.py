from crypt import methods
from curses import echo
from flask import redirect, render_template, url_for, flash, request, session, current_app
from loja import db, app

@app.route('/addcart', methods=["POST"])
def addCart():
    try:
        pass
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)