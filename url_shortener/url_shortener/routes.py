from flask import Blueprint, render_template, request, redirect

from .extensions import db
from .models import Link
from .auth import requires_auth
import sys

short = Blueprint('short', __name__)



@short.route('/<short_url>')#this func helper to connect with a orginal url
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1# i added this step to counter how many visits in page
    db.session.commit()

    return redirect(link.original_url) 

@short.route('/')
@requires_auth

def index():
    return render_template('index.html') 

@short.route('/add_link', methods=['POST'])
@requires_auth
def add_link():# add url to database and appear that in web

    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html',
                           new_link=link.short_url, original_url=link.original_url)



@short.route('/stats')
@requires_auth
def stats():# status and get all data for evrey element
    links = Link.query.all()

    return render_template('stats.html', links=links)

def checkIfURLIsExist(theLink):
    links = Link.query.all()
    temp = ""
    for link in links:

        if (link.original_url == theLink):
            return True;
        else :
            return False


@short.route('/return_link', methods=['POST'])# this for short to orginal url
@requires_auth
def return_link():
    links = Link.query.all()

    shorter_url = request.form['shorter_url']
    tempForShort = " "# temperate String to put short URL
    tempForOriginal = ""

    for link in links:
        tempForOriginal = "http://localhost:5000/"+link.short_url


        if (tempForOriginal == shorter_url):
            tempForShort = link.original_url
            break
        else :
            tempForShort = "false"


    return render_template('returning_link.html',
        new_link= tempForShort ,original_url=tempForOriginal)



@short.route('/longurl', methods=['GET','POST'])



@short.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404