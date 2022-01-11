from flask import Flask, render_template
from markupsafe import escape
import pymongo
import os
from waitress import serve

app = Flask(__name__, static_url_path='')

atlashost = os.environ['ATLAS_HOST']
atlasusr = os.environ['ATLAS_USERNAME']
atlaspwd = os.environ['ATLAS_PASSWORD']
atlasdb = os.environ['ATLAS_DB']
gmapskey = os.environ['GMAPS_KEY']

client = pymongo.MongoClient("mongodb+srv://" + atlasusr + ":" + atlaspwd + "@" + atlashost + "/" + atlasdb + "?retryWrites=true&w=majority")
db = client.mystrk
coll = db.tracks
trk = coll.find_one()

@app.route("/")
def index():
    # return app.send_static_file('index.html')
    return render_template('index.html.jinja', name=trk, googlemapskey=GMAPS_KEY)

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

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)

