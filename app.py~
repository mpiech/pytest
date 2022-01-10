from flask import Flask, render_template
from markupsafe import escape
import pymongo
import dns

app = Flask(__name__, static_url_path='')

# AIzaSyARqfACf-Q-48tihr5CLHnRdrPKPQ2L984

client = pymongo.MongoClient("mongodb+srv://atlas-db-user-1641355160695861880:a1)9=25v@cluster0.brwd1.mongodb.net/mystrk?retryWrites=true&w=majority")
db = client.mystrk
coll = db.tracks
trk = coll.find_one()


@app.route("/")
def index():
    # return app.send_static_file('index.html')
    return render_template('index.html.jinja', name=trk, googlemapskey="AIzaSyARqfACf-Q-48tihr5CLHnRdrPKPQ2L984")

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

